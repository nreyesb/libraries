# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: path_sanitizer_storage_driver_decorator.py
Author: Toku Dev
"""
from io import BufferedReader
from typing import Optional
from overrides import override
from toku.storage.driver.api import PathSanitizer
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.api import StorageDriverDecorator


class PathSanitizerStorageDriverDecorator(StorageDriverDecorator):
    """
    Provides a decorator to wrap the DirectorySeparator enum and ensure
    that each path used as a parameter or obtained by a method is consistent with
    the DirectorySeparator of the storage driver.
    """

    def __init__(self, storage_driver: StorageDriver) -> None:
        """
        Initialize the internal 'sanitizer' with the directory separator of
        the 'storage_driver'.
        """
        super().__init__(storage_driver)
        self._sanitizer = PathSanitizer(storage_driver.get_separator())

    @override
    def open(self) -> None:
        self._storage_driver.open()

    @override
    def close(self) -> None:
        self._storage_driver.close()

    @override
    def get(self, file: str) -> Optional[bytes]:
        return self._storage_driver.get(self._sanitizer.sanitize(file, True))

    @override
    def get_as_input_stream(self, file: str) -> Optional[BufferedReader]:
        return self._storage_driver.get_as_input_stream(self._sanitizer.sanitize(file, True))

    @override
    def exists(self, file: str) -> bool:
        return self._storage_driver.exists(self._sanitizer.sanitize(file, True))

    @override
    def put_file(self, source: bytes | str | BufferedReader, directory: str) -> Optional[str]:
        if isinstance(source, str):
            return self._storage_driver.put_file(
                self._sanitizer.sanitize(source, True), self._sanitizer.sanitize(directory, True)
            )

        return self._storage_driver.put_file(source, self._sanitizer.sanitize(directory, True))

    @override
    def put_file_as(self, source: bytes | str | BufferedReader, file: str) -> bool:
        if isinstance(source, str):
            return self._storage_driver.put_file_as(
                self._sanitizer.sanitize(source, True), self._sanitizer.sanitize(file, True)
            )

        return self._storage_driver.put_file_as(source, self._sanitizer.sanitize(file, True))

    @override
    def append(self, source: bytes, file: str) -> bool:
        return self._storage_driver.append(source, self._sanitizer.sanitize(file, True))

    @override
    def copy(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if not target_storage_driver:
            return self._storage_driver.copy(
                self._sanitizer.sanitize(source, True),
                self._sanitizer.sanitize(target, True)
            )

        return self._storage_driver.copy(
            self._sanitizer.sanitize(source, True),
            self._sanitizer.sanitize(target, True),
            target_storage_driver
        )

    @override
    def move(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if not target_storage_driver:
            return self._storage_driver.move(
                self._sanitizer.sanitize(source, True),
                self._sanitizer.sanitize(target, True)
            )

        return self._storage_driver.move(
            self._sanitizer.sanitize(source, True),
            self._sanitizer.sanitize(target, True),
            target_storage_driver
        )

    @override
    def delete(self, file: str) -> bool:
        return self._storage_driver.delete(self._sanitizer.sanitize(file, True))

    @override
    def rename(self, source: str, target: str) -> bool:
        return self._storage_driver.rename(
            self._sanitizer.sanitize(source, True),
            self._sanitizer.sanitize(target, True)
        )

    @override
    def files(self, directory: str) -> list[str]:
        sanitized_directory: str = self._sanitizer.sanitize(directory, True)
        files: list[str] = self._storage_driver.files(sanitized_directory)
        return [self._sanitizer.sanitize(file, True) for file in files]

    @override
    def all_files(self, directory: str) -> list[str]:
        sanitized_directory: str = self._sanitizer.sanitize(directory, True)
        files: list[str] = self._storage_driver.all_files(sanitized_directory)
        return [self._sanitizer.sanitize(file, True) for file in files]

    @override
    def directories(self, directory: str) -> list[str]:
        sanitized_directory: str = self._sanitizer.sanitize(directory, True)
        directories: list[str] = self._storage_driver.directories(sanitized_directory)
        return [self._sanitizer.sanitize(directory, True) for directory in directories]

    @override
    def all_directories(self, directory: str) -> list[str]:
        sanitized_directory: str = self._sanitizer.sanitize(directory, True)
        directories: list[str] = self._storage_driver.all_directories(sanitized_directory)
        return [self._sanitizer.sanitize(directory, True) for directory in directories]

    @override
    def exists_directory(self, directory: str) -> bool:
        return self._storage_driver.exists_directory(self._sanitizer.sanitize(directory, True))

    @override
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if not target_storage_driver:
            return self._storage_driver.copy_directory(
                self._sanitizer.sanitize(source, True),
                self._sanitizer.sanitize(target, True)
            )

        return self._storage_driver.copy_directory(
            self._sanitizer.sanitize(source, True),
            self._sanitizer.sanitize(target, True),
            target_storage_driver
        )

    @override
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if not target_storage_driver:
            return self._storage_driver.move_directory(
                self._sanitizer.sanitize(source, True),
                self._sanitizer.sanitize(target, True)
            )

        return self._storage_driver.move_directory(
            self._sanitizer.sanitize(source, True),
            self._sanitizer.sanitize(target, True),
            target_storage_driver
        )

    @override
    def make_directory(self, directory: str) -> bool:
        return self._storage_driver.make_directory(self._sanitizer.sanitize(directory, True))

    @override
    def delete_directory(self, directory: str) -> bool:
        return self._storage_driver.delete_directory(self._sanitizer.sanitize(directory, True))

    @override
    def rename_directory(self, source: str, target: str) -> bool:
        return self._storage_driver.rename_directory(
            self._sanitizer.sanitize(source, True), self._sanitizer.sanitize(target, True)
        )

    @override
    def get_metadata(self, path: str) -> Optional[Metadata]:
        return self._storage_driver.get_metadata(self._sanitizer.sanitize(path, True))

    @override
    def get_root(self) -> str:
        return self._storage_driver.get_root()

    @override
    def get_separator(self) -> DirectorySeparator:
        return self._storage_driver.get_separator()
