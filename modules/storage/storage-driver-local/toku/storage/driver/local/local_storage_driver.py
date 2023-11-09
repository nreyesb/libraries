# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: local_storage_driver.py
Author: Toku
"""
import glob
from io import BufferedReader
import os
import platform
import shutil
from typing import final
from overrides import override
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import Size
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import AbstractStorageDriver
from toku.storage.driver.api import StorageDriverException


@final
class LocalStorageDriver(AbstractStorageDriver):
    """
    Provides the storage driver to work locally, it's necessary that the running
    instance application has the access to work within the `root`.
    """

    def __init__(
            self,
            root: str,
            separator: DirectorySeparator = DirectorySeparator.SLASH
    ) -> None:
        """
        Initializes a new Local storage driver.

        Args:
            root (str): The working directory.
            separator (DirectorySeparator): The directory separator.
                                            Defaults to DirectorySeparator.SLASH.
        """
        super().__init__(root, separator)

    @override
    def open(self) -> None:
        if not os.path.isdir(self._root):
            raise StorageDriverException(f"root {self._root} is not a directory")

    @override
    def close(self) -> None:
        # this process works in a local directory,
        # it's not needed to do anything to close the driver
        pass

    @override
    def _get_as_input_stream(self, file: str) -> BufferedReader:
        return open(self._get_path(file), "rb")

    @override
    def exists(self, file: str) -> bool:
        return os.path.isfile(self._get_path(file))

    @override
    def _put_file_as(self, source: BufferedReader, file: str) -> bool:
        with open(self._get_path(file), "wb") as target:
            shutil.copyfileobj(source, target)
            return True

    @override
    def _append(self, source: bytes, file: str) -> bool:
        with open(self._get_path(file), "ab") as target:
            target.write(source)
            return True

    @override
    def _delete(self, file: str) -> bool:
        os.remove(self._get_path(file))
        return True

    @override
    def _rename(self, source: str, target: str) -> bool:
        os.rename(self._get_path(source), self._get_path(target))
        return True

    @override
    def _files(self, directory: str) -> list[str]:
        directory_path: str = self._get_path(directory)
        return [
            self._sanitizer.sanitize(file_path.replace(self._root, ""), True)
            for file_path in glob.glob(f"{directory_path}/*")
            if os.path.isfile(file_path)
        ]

    @override
    def _all_files(self, directory: str) -> list[str]:
        directory_path: str = self._get_path(directory)
        return [
            self._sanitizer.sanitize(file_path.replace(self._root, ""), True)
            for file_path in glob.glob(f"{directory_path}/**/*", recursive=True)
            if os.path.isfile(file_path)
        ]

    @override
    def _directories(self, directory: str) -> list[str]:
        directory_path: str = self._get_path(directory)
        return [
            self._sanitizer.sanitize(file_path.replace(self._root, ""), True)
            for file_path in glob.glob(f"{directory_path}/*")
            if os.path.isdir(file_path)
        ]

    @override
    def _all_directories(self, directory: str) -> list[str]:
        directory_path: str = self._get_path(directory)
        return [
            self._sanitizer.sanitize(file_path.replace(self._root, ""), True)
            for file_path in glob.glob(f"{directory_path}/**/*", recursive=True)
            if os.path.isdir(file_path)
        ]

    @override
    def exists_directory(self, directory: str) -> bool:
        return os.path.isdir(self._get_path(directory))

    @override
    def _make_directory(self, directory: str) -> bool:
        os.makedirs(self._get_path(directory), exist_ok=True)
        return True

    @override
    def _delete_directory(self, directory: str) -> bool:
        shutil.rmtree(self._get_path(directory), ignore_errors=True)
        return True

    @override
    def _rename_directory(self, source: str, target: str) -> bool:
        return self._rename(source, target)

    @override
    def _get_metadata_from_file(self, file: str) -> Metadata:
        file_path: str = self._get_path(file)
        os_stat = os.stat(file_path)
        return Metadata(
            size=Size(os_stat.st_size),
            creation_time=int(
                os_stat.st_ctime
                if platform.system() == 'Windows'
                else os_stat.st_birthtime
            ),
            last_modified=int(os_stat.st_mtime),
            last_access_time=int(os_stat.st_atime),
            is_file=os.path.isfile(file_path),
            is_directory=os.path.isdir(file_path),
            is_symbolic_link=os.path.islink(file_path),
            media_type=Metadata.detect_media_type(file_path)
        )

    @override
    def _get_metadata_from_directory(self, directory: str) -> Metadata:
        directory_path: str = self._get_path(directory)
        files_metadata: list[Metadata] = [
            self._get_metadata_from_file(f) for f in self._all_files(directory)
        ]
        os_stat = os.stat(directory_path)
        return Metadata(
            size=Size(sum(m.size.length for m in files_metadata)),
            creation_time=int(
                os_stat.st_ctime
                if platform.system() == 'Windows'
                else os_stat.st_birthtime
            ),
            last_modified=int(os_stat.st_mtime),
            last_access_time=int(os_stat.st_atime),
            is_file=os.path.isfile(directory_path),
            is_directory=os.path.isdir(directory_path),
            is_symbolic_link=os.path.islink(directory_path),
            media_type=""
        )

    def _get_path(self, path: str) -> str:
        return self._sanitizer.concat(self._root, path)
