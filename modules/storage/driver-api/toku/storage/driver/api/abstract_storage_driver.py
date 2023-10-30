# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: abstract_storage_driver.py
Author: Toku Dev
"""
import uuid
from typing import Callable, Optional
from io import BytesIO, BufferedReader
from abc import ABC, abstractmethod
from overrides import override
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import PathSanitizer
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import StorageDriver


class AbstractStorageDriver(StorageDriver, ABC):
    """
    The `AbstractStorageDriver` class provides a base for working with storage drivers.

    All methods using the pattern `{method}_internal` provide the specific logic to
    execute the final action of similar processes.
    """

    def __init__(self, root: str, separator: DirectorySeparator) -> None:
        """
        Initializes a new abstract storage driver.

        Args:
            root (str): The working directory.
            separator (DirectorySeparator): The separator of the directories.
        """
        self._sanitizer: PathSanitizer = PathSanitizer(separator)
        self._root: str = self._sanitizer.sanitize(root)
        self._separator: DirectorySeparator = separator

    @override
    def get(self, file: str) -> Optional[bytes]:
        data: Optional[BufferedReader] = self.get_as_input_stream(file)

        if not data:
            return None

        with data as input_stream:
            return input_stream.read()

    @override
    def get_as_input_stream(self, file: str) -> Optional[BufferedReader]:
        return self._get_as_input_stream_internal(file) if self.exists(file) else None

    @abstractmethod
    def _get_as_input_stream_internal(self, file: str) -> BufferedReader:
        """
        Provide the process to get a BufferedReader object as an input stream from a file.

        Args:
            file (str): Full file path.

        Returns:
            BufferedReader: The input stream internal.
        """

    @override
    def put_file(self, source: bytes | str | BufferedReader, directory: str) -> Optional[str]:
        file_name: str = str(uuid.uuid4()).lower()
        file = file_name \
            if not directory or not directory.strip() \
            else self._sanitizer.concat(directory, file_name)

        if self.put_file_as(source, file):
            return file_name

        return None

    @override
    def put_file_as(self, source: bytes | str | BufferedReader, file: str) -> bool:
        if not source:  # source is None
            return False

        if not file or not file.strip():  # file is empty
            return False

        if self.exists_directory(file):  # file is directory
            return False

        if self.exists(self._sanitizer.get_parent(file)):  # file parent folder is a file
            return False

        parent: str = self._sanitizer.get_parent(file)

        # create parent if not exists and not root
        if parent and \
           parent.strip() and \
           not self.exists_directory(parent) and \
           not self.make_directory(parent):
            return False

        # put the file
        if isinstance(source, str):
            with open(source, "rb") as f:
                return self._put_file_as_internal(f, file)

        input_stream: BufferedReader

        if isinstance(source, bytes):
            bytes_handle = BytesIO(source)
            input_stream = BufferedReader(bytes_handle)  # type: ignore[arg-type]
        else:
            input_stream = source

        return self._put_file_as_internal(input_stream, file)

    @abstractmethod
    def _put_file_as_internal(self, source: BufferedReader, file: str) -> bool:
        """
        Provide the process to put the content from source into a file.

        Args:
            source (Union[bytes, str, BufferedReader]): The content to be put into the file.
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def append(self, source: bytes, file: str) -> bool:
        if not source:  # source is None
            return False

        if not self.exists(file):  # file doesn't exist
            return False

        return self._append_internal(source, file)

    @abstractmethod
    def _append_internal(self, source: bytes, file: str) -> bool:
        """
        Provide the process to append content to a file.

        Args:
            source (bytes): Content as byte arrays.
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def copy(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        target_storage_driver = self if not target_storage_driver else target_storage_driver

        if not source or not source.strip() or self.exists_directory(source):  # source is directory
            return False

        if not self.exists(source):  # source doesn't exist
            return False

        if not target or \
           not target.strip() or \
           target_storage_driver.exists_directory(target):  # target is a directory
            return False

        if self == target_storage_driver and \
           source == target:  # source equals to target in the same driver
            return False

        if target_storage_driver.exists(target) and \
           not target_storage_driver.delete(target):  # delete if exists
            return False

        with self._get_as_input_stream_internal(source) as input_stream:
            return target_storage_driver.put_file_as(input_stream, target)

    @override
    def move(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if self.copy(source, target, target_storage_driver):
            return self._delete_internal(source)

        return False

    @override
    def delete(self, file: str) -> bool:
        if not self.exists(file):  # file doesn't exist
            return False

        if self.exists_directory(file):  # file is directory
            return False

        return self._delete_internal(file)

    @abstractmethod
    def _delete_internal(self, file: str) -> bool:
        """
        Provide the process to delete a file.

        Args:
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def rename(self, source: str, target: str) -> bool:
        if not self.exists(source):  # source doesn't exist
            return False

        if not source or not source.strip() or self.exists_directory(source):  # source is directory
            return False

        if self.exists(target):  # target exists
            return False

        if not target or \
           not target.strip() or \
           self.exists_directory(target):  # target is a directory
            return False

        if source == target:  # source equals to target
            return False

        return self._rename_internal(source, target)

    @abstractmethod
    def _rename_internal(self, source: str, target: str) -> bool:
        """
        Provide the process to rename a file from source to target.

        Args:
            source (str): Full file path of the source.
            target (str): Full file path of the target.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def files(self, directory: str) -> list[str]:
        return self.files_or_directories(directory, self._files_internal)

    @abstractmethod
    def _files_internal(self, directory: str) -> list[str]:
        """
        Provide the process to get the files in the specified directory.

        Args:
            directory (str): The directory to get files from.

        Returns:
            list[str]: List of files in the directory.
        """

    @override
    def all_files(self, directory: str) -> list[str]:
        return self.files_or_directories(directory, self._all_files_internal)

    @abstractmethod
    def _all_files_internal(self, directory: str) -> list[str]:
        """
        Provide the process to get all files, recursively, in the specified directory.

        Args:
            directory (str): The directory to get files from.

        Returns:
            list[str]: List of all files in the directory and its subdirectories.
        """

    @override
    def directories(self, directory: str) -> list[str]:
        return self.files_or_directories(directory, self._directories_internal)

    @abstractmethod
    def _directories_internal(self, directory: str) -> list[str]:
        """
        Provide the process to get the directories in the specified directory.

        Args:
            directory (str): The directory to get subdirectories from.

        Returns:
            list[str]: List of subdirectories in the directory.
        """

    @override
    def all_directories(self, directory: str) -> list[str]:
        return self.files_or_directories(directory, self._all_directories_internal)

    @abstractmethod
    def _all_directories_internal(self, directory: str) -> list[str]:
        """
        Provide the process to get all directories, recursively, in the specified directory.

        Args:
            directory (str): The directory to get subdirectories from.

        Returns:
            list[str]: List of all subdirectories in the directory and its subdirectories.
        """

    def files_or_directories(
        self,
        directory: str,
        get_resources: Callable[[str], list[str]]
    ) -> list[str]:
        """
        Provides the standard process to get files or directories from a directory,
        the process to get the resources is provided by the get_resources function.

        Args:
            directory (str): Directory to search for files or directories.
            get_resources (Callable[[str], list[str]]): The process to get the files or directories.

        Returns:
            list[str]: A list of file or directory paths.
        """
        if not self.exists_directory(directory):  # directory doesn't exist
            return []

        if self.exists(directory):  # directory is file
            return []

        return get_resources(directory)

    @override
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        return self._copy_or_move_directory(source, target, False, target_storage_driver)

    @override
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        return self._copy_or_move_directory(source, target, True, target_storage_driver)

    def _copy_or_move_directory(
        self,
        source: str,
        target: str,
        remove_source: bool,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        """
        Provide the process to copy or move each file in `source` to `target`
        including its subdirectories.

        If `target_storage_driver` is None then the same storage driver is used.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            remove_source (bool): Removes the folder / file after finishing the action
            target_storage_driver (Optional['StorageDriver']): Storage driver to use
                                                               in the target. Defaults to None.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """
        target_storage_driver = self if not target_storage_driver else target_storage_driver

        if not source or not source.strip():  # source is root
            return False

        if not self.exists_directory(source):  # source doesn't exist
            return False

        if self.exists(source):  # source is file
            return False

        if self._sanitizer.get_parent(source) == target:  # source parent directory is target
            return False

        if self._sanitizer.add_directory_separator(target) \
            .startswith(
                self._sanitizer.add_directory_separator(source)
                ):  # source is part of parent in target
            return False

        if not target_storage_driver.exists_directory(target):  # target not exists
            return False

        if target_storage_driver.exists(target):  # target is file
            return False

        return self._transfer_files(
            source,
            target,
            remove_source,
            target_storage_driver
        )

    def _transfer_files(
        self,
        source: str,
        target: str,
        remove_source: bool,
        target_storage_driver: StorageDriver
    ) -> bool:
        """
        Transfer all the files from `source` to `target` removing each file and the
        `source` folder itself if `remove_source` is True.

        `target_storage_driver` is the target storage driver where each file will
        be copied or moved.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            remove_source (bool): Removes the folder / file after finishing the action
            target_storage_driver (StoragaDriver): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """
        # get source parent
        source_parent: str = self._sanitizer.get_parent(source)

        # copy files of the directory
        for file in self._all_files_internal(source):
            file_path: str = self._sanitizer.sanitize(
                self._sanitizer.sanitize(file).replace(source_parent, ""),
                True
            )
            target_path: str = \
                file_path \
                if not target or not target.strip() \
                else self._sanitizer.concat(target, file_path)

            with self._get_as_input_stream_internal(file) as input_stream:
                if not target_storage_driver.put_file_as(input_stream, target_path):
                    return False
                if remove_source and not self.delete(file):
                    return False

        # if remove_source is true then delete the folder
        if remove_source:
            return self._delete_directory_internal(source)

        return True

    @override
    def make_directory(self, directory: str) -> bool:
        if not directory or not directory.strip():  # directory is root
            return False

        if self.exists_directory(directory):  # directory exists
            return False

        if self.exists(directory):  # directory is file
            return False

        return self._make_directory_internal(directory)

    @abstractmethod
    def _make_directory_internal(self, directory: str) -> bool:
        """
        Provide the process to create a directory.

        Args:
            directory (str): Full directory path.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def delete_directory(self, directory: str) -> bool:
        if not directory or not directory.strip():  # directory is root
            return False

        if not self.exists_directory(directory):  # directory doesn't exist
            return False

        if self.exists(directory):  # directory is file
            return False

        return self._delete_directory_internal(directory)

    @abstractmethod
    def _delete_directory_internal(self, directory: str) -> bool:
        """
        Provide the process to delete a directory.

        Args:
            directory (str): Full directory path.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def rename_directory(self, source: str, target: str) -> bool:
        if not source or not source.strip():  # source is root
            return False

        if not self.exists_directory(source):  # source doesn't exist
            return False

        if self.exists(source):  # source is file
            return False

        if not target or not target.strip():  # target is root
            return False

        if self.exists_directory(target):  # target is a directory
            return False

        if self.exists(target):  # target is file
            return False

        if source == target:  # source equals to target
            return False

        return self._rename_directory_internal(source, target)

    @abstractmethod
    def _rename_directory_internal(self, source: str, target: str) -> bool:
        """
        Provide the process to rename a directory from source to target.

        Args:
            source (str): Full directory path of the source.
            target (str): Full directory path of the target.

        Returns:
            bool: True if the action could be executed, False otherwise.
        """

    @override
    def get_metadata(self, path: str) -> Optional[Metadata]:
        if self.exists(path):
            return self._get_metadata_from_file(path)

        if self.exists_directory(path):
            return self._get_metadata_from_directory(path)

        return None

    @abstractmethod
    def _get_metadata_from_file(self, file: str) -> Metadata:
        """
        Get metadata from a file.

        Args:
            file (str): The full file path.

        Returns:
            Metadata: The metadata for the file.
        """

    @abstractmethod
    def _get_metadata_from_directory(self, directory: str) -> Metadata:
        """
        Get metadata from a directory.

        Args:
            directory (str): The full directory path.

        Returns:
            Metadata: The metadata for the directory.
        """

    @override
    def get_root(self) -> str:
        return self._root

    @override
    def get_separator(self) -> DirectorySeparator:
        return self._separator

    @override
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, type(self)) and self._root == obj._root
