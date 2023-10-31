# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: gcs_storage_driver.py
Author: Toku Dev
"""
from io import BufferedReader, BytesIO
import os
from tempfile import NamedTemporaryFile
import time
from typing import final
from google.oauth2 import service_account  # type:ignore[import-untyped]
from google.cloud import storage  # type:ignore[import-untyped]
from overrides import override
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import Size
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import AbstractStorageDriver
from toku.storage.driver.api import StorageDriverException


@final
class CustomBufferedReader(BufferedReader):
    """
    Helper BufferedReader to wrap a file a return it as an input stream,
    finally after reading it the file is deleted from the local disk.
    """

    def __init__(  # type:ignore[no-untyped-def]
            self,
            file
    ) -> None:
        """
        Starts the wrapper buffered reader with the temporal file `file`.
        """
        super().__init__(open(file.name, 'rb'))  # type:ignore[arg-type]
        self._file = file

    def __exit__(  # type:ignore[no-untyped-def]
            self,
            exc_type,
            exc_value,
            traceback
    ) -> None:
        """
        Close the buffered reader (the object created after opened the file)
        and remove the temporal file itself from the local disk.
        """
        try:
            self.close()
            self._file.close()
        finally:
            os.remove(self._file.name)


@final
class GcsStorageDriver(AbstractStorageDriver):
    """
    Provides the storage driver to work with Google Cloud Storage (a blob storage),
    it's necessary that the service account has the the access to work within
    the `bucket` for the `project`.
    """

    def __init__(
            self,
            root: str,
            project_id: str,
            bucket_name: str,
            credentials_file: str
    ) -> None:
        """
        Initializes a new GCS (Google Cloud Storage) storage driver.

        Args:
            root (str): The working directory (without the bucket name).
            project_id (str): The GCP (Google Cloud Platform) project ID.
            bucket_name (str): The name of the bucket.
            credentials_file (str): The path to the credential file. It's recommended to
                                    use a service account.
        """
        super().__init__(root, DirectorySeparator.SLASH)
        self._project_id: str = project_id
        self._bucket_name: str = bucket_name
        self._credentials_file: str = credentials_file

    @override
    def open(self) -> None:
        credentials = service_account.Credentials.from_service_account_file(self._credentials_file)

        if credentials.project_id != self._project_id:
            raise StorageDriverException(
                f"service account project {credentials.project_id} and "
                f"cloud storage project {self._project_id} are not the same"
            )

        self._storage = storage.Client(  # pylint: disable=attribute-defined-outside-init
            project=self._project_id,
            credentials=credentials
        )
        self._bucket = self._storage.bucket(self._bucket_name)  # pylint: disable=attribute-defined-outside-init

        if not self._bucket.exists():
            raise StorageDriverException(
                f"bucket {self._bucket_name} doesn't exists "
                f"in project {self._project_id}"
            )

    @override
    def close(self) -> None:
        self._storage.close()

    @override
    def _get_as_input_stream(self, file: str) -> BufferedReader:
        # the process copies the blob to a local file to avoid loading the
        # whole content in memory (poor perfomance), on that way it can return
        # a buffered reader from a temporal file in the local disk and delete
        # it after reading, to do that the CustomBufferedReader class extends
        # the BufferedReader class to wrap the temporal file and the input
        # stream, finally in the __exit__ method it delete the file.
        blob = self._create_blob(file)

        with NamedTemporaryFile(delete=False) as temp_file:
            blob.download_to_file(temp_file)

        return CustomBufferedReader(temp_file)

    @override
    def exists(self, file: str) -> bool:
        blob = self._create_blob(file)
        return blob.exists() and not blob.name.endswith("/")

    @override
    def _put_file_as(self, source: BufferedReader, file: str) -> bool:
        blob = self._create_blob(file)
        blob.upload_from_file(source)
        return True

    @override
    def _append(self, source: bytes, file: str) -> bool:
        append_blob_path = f"{file}.append{str(int(time.time() * 1000))}"
        self._put_file_as(
            BufferedReader(BytesIO(source)), append_blob_path  # type: ignore[arg-type]
        )
        try:
            target_blob = self._create_blob(file)
            append_blob = self._create_blob(append_blob_path)
            target_blob.compose([target_blob, append_blob])
            return True
        finally:
            self._delete(append_blob_path)

    @override
    def _delete(self, file: str) -> bool:
        blob = self._create_blob(file)
        blob.delete()
        self._check_parent_directory_and_create(file)
        return True

    @override
    def _rename(self, source: str, target: str) -> bool:
        blob = self._create_blob(source)
        self._bucket.rename_blob(blob, self._add_root_in_path(target))
        return self.exists(target)

    @override
    def _files(self, directory: str) -> list[str]:
        # `delimiter` is used to get only the files in the `directory`
        blobs = self._bucket.list_blobs(
            prefix=self._add_root_in_path(directory, True),
            delimiter=self._separator.value
        )
        return [
            self._remove_root_in_path(blob.name)
            for blob in blobs
            if not blob.name.endswith("/") and
            self._sanitizer.sanitize(directory) !=
            self._sanitizer.sanitize(self._remove_root_in_path(blob.name))
        ]

    @override
    def _all_files(self, directory: str) -> list[str]:
        blobs = self._bucket.list_blobs(
            prefix=self._add_root_in_path(directory, True)
        )
        return [
            self._remove_root_in_path(blob.name)
            for blob in blobs
            if not blob.name.endswith("/") and
            self._sanitizer.sanitize(directory) !=
            self._sanitizer.sanitize(self._remove_root_in_path(blob.name))
        ]

    @override
    def _directories(self, directory: str) -> list[str]:
        # `match_glob` is used to get only the directories in the `directory`
        blobs = self._bucket.list_blobs(
            prefix=self._add_root_in_path(directory, True),
            match_glob=f"{self._add_root_in_path(directory, True)}*{self._separator.value}"
        )
        return [
            self._remove_root_in_path(blob.name)
            for blob in blobs
            if blob.name.endswith("/") and
            self._sanitizer.sanitize(directory) !=
            self._sanitizer.sanitize(self._remove_root_in_path(blob.name))
        ]

    @override
    def _all_directories(self, directory: str) -> list[str]:
        blobs = self._bucket.list_blobs(
            prefix=self._add_root_in_path(directory, True)
        )
        return [
            self._remove_root_in_path(blob.name)
            for blob in blobs
            if blob.name.endswith("/") and
            self._sanitizer.sanitize(directory) !=
            self._sanitizer.sanitize(self._remove_root_in_path(blob.name))
        ]

    @override
    def exists_directory(self, directory: str) -> bool:
        blob = self._create_blob(directory, True)
        return blob.exists() and blob.name.endswith("/") is True

    @override
    def _make_directory(self, directory: str) -> bool:
        # the directory concept doesn't exists in cloud storage, so to
        # emulate the behavior it's possible to use a '/' with a empty
        # content, if the '/' doesn't have an empty content the API
        # doesn't recognize that exists, then to ensure that every
        # directory "exists" the process try to create all directories
        # that the path has asking if it exists with `blob.exists()`
        elements: list[str] = directory.split(self._separator.value)
        directory_to_create = ""

        for element in elements:
            directory_to_create = element \
                if directory_to_create == "" \
                else f"{directory_to_create}{self._separator.value}{element}"
            blob = self._create_blob(directory_to_create, True)
            if not blob.exists():
                blob.upload_from_string(b"")

        return True

    @override
    def _delete_directory(self, directory: str) -> bool:
        # delete all files
        # the list need to return only a True or empty to continue processing
        deleted_files_result: list[bool] = list(set(
            self._delete(file)
            for file in self._all_files(directory)
        ))

        if deleted_files_result and \
           (len(deleted_files_result) > 1 or not deleted_files_result[0]):
            return False

        # delete all directories
        # the list need to return only a True or empty to continue processing
        deleted_directories_result: list[bool] = list(set(
            self._delete_directory(d)
            for d in self._all_directories(directory)
        ))

        if deleted_directories_result and \
           (len(deleted_directories_result) > 1 or not deleted_directories_result[0]):
            return False

        # delete itself
        if self.exists_directory(directory):
            blob = self._create_blob(directory, True)
            blob.delete()
            self._check_parent_directory_and_create(directory)
        return True

    @override
    def _rename_directory(self, source: str, target: str) -> bool:
        if self._make_directory(target):
            for file in self._all_files(source):
                target_path: str = self._sanitizer.concat(
                    target,
                    file.replace(self._sanitizer.add_directory_separator(source), "")
                )

                if not self._rename(file, target_path):
                    return False
            return self._delete_directory(source)
        return False

    @override
    def _get_metadata_from_file(self, file: str) -> Metadata:
        # it uses `bucket.get_blob` instead of `bucket.blob` to get
        # the metadata at the same moment because `blob` method only
        # create a reference to the blob and it's lazy
        blob = self._bucket.get_blob(self._add_root_in_path(file))
        return Metadata(
            size=Size(blob.size),
            creation_time=blob.time_created.timestamp(),
            last_modified=blob.updated.timestamp(),
            last_access_time=blob.updated.timestamp(),
            is_file=True,
            is_directory=False,
            is_symbolic_link=False,
            media_type=Metadata.detect_media_type(file)
        )

    @override
    def _get_metadata_from_directory(self, directory: str) -> Metadata:
        metadatas = [self._get_metadata_from_file(f) for f in self._all_files(directory)]
        return Metadata(
            size=Size(sum(m.size.length for m in metadatas)),
            creation_time=min(m.creation_time for m in metadatas),
            last_modified=max(m.last_modified for m in metadatas),
            last_access_time=max(m.last_access_time for m in metadatas),
            is_file=False,
            is_directory=True,
            is_symbolic_link=False,
            media_type=""
        )

    def _add_root_in_path(
            self,
            path: str,
            add_directory_separator: bool = False
    ) -> str:
        """
        Adds the root in path.

        Generates a new path by concatenating the `self._root` and `path`.

        The final path is sanitized and includes the directory separator if
        `add_directory_separator` is True.

        Args:
            path (str): The path.
            add_directory_separator (bool): Whether to add a directory separator. Default is False.

        Returns:
            str: The concatenated root and path.
        """
        return (
            f"{self._sanitizer.concat(self._root, path)}"
            f"{self._separator.value if add_directory_separator else ''}"
        )

    def _remove_root_in_path(self, path: str) -> str:
        """
        Removes the root in path.

        Generates a new path by removing the `self._root` from `path`.

        The final path is sanitized by removing the directory separator at the
        beginning of the path.

        Args:
            path (str): The path.

        Returns:
            str: The path without the root.
        """
        return self._sanitizer.sanitize(
            self._sanitizer.sanitize(path).replace(self._root, ""), True
        )

    def _create_blob(  # type:ignore[no-any-unimported]
            self,
            object_name: str,
            add_directory_separator: bool = False
    ) -> storage.Blob:
        """
        Creates the blob.

        Creates a Blob with `self._bucket`and the `object_name`.

        If `add_directory_separator` is True, a directory separator is added.

        It uses `self._bucket.blob` instead of `self._bucket.get_blob` bacause
        it needs only the reference not the metadata for every process.

        Args:
            object_name (str): The object name.
            add_directory_separator (bool): Whether to add a directory separator. Defaults to False.

        Returns:
            Blob: The blob id.
        """
        return self._bucket.blob(
            self._add_root_in_path(object_name, add_directory_separator)
        )

    def _check_parent_directory_and_create(self, path: str) -> None:
        """
        Check parent directory and create.

        Check if the parent directory of the given `path` exists, and if it doesn't
        then create it. If the `path` is blank or equal to the directory separator,
        then the process ends.

        Args:
            path (str): The path.
        """
        if path and path.strip() != self._separator.value:
            directory: str = self._sanitizer.get_parent(path)

            if not self.exists_directory(directory) and \
               not self._make_directory(directory):
                raise StorageDriverException(f"Could not create the parent directory {directory}")
