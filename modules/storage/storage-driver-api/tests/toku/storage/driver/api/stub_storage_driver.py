# -*- coding: utf-8 -*-
# pylint: disable=unused-argument
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: stub_storage_driver.py
Author: Toku Dev
"""
from io import BufferedReader
from typing import Optional
from overrides import override
from toku.storage.driver.api import StorageDriver, DirectorySeparator, Metadata


class StubStorageDriver(StorageDriver):
    """
    A stub that provided default behavior, where any null is returned for any method.
    """

    def __init__(self, separator: DirectorySeparator = DirectorySeparator.SLASH) -> None:
        """_summary_

        Args:
            separator (DirectorySeparator): The directory separator.
                                            Defaults to DirectorySeparator.SLASH.
        """
        self._separator: DirectorySeparator = separator

    @override
    def close(self) -> None:
        pass  # logic not needed

    @override
    def open(self) -> None:
        pass  # logic not needed

    @override
    def get(self, file: str) -> Optional[bytes]:
        return None

    @override
    def get_as_input_stream(self, file: str) -> Optional[BufferedReader]:
        return None

    @override
    def exists(self, file: str) -> bool:
        return False

    @override
    def put_file(self, source: bytes | str | BufferedReader, directory: str) -> Optional[str]:
        return None

    @override
    def put_file_as(self, source: bytes | str | BufferedReader, file: str) -> bool:
        return False

    @override
    def append(self, source: bytes, file: str) -> bool:
        return False

    @override
    def copy(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional[StorageDriver] = None
    ) -> bool:
        return False

    @override
    def move(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional[StorageDriver] = None
    ) -> bool:
        return False

    @override
    def delete(self, file: str) -> bool:
        return False

    @override
    def rename(self, source: str, target: str) -> bool:
        return False

    @override
    def files(self, directory: str) -> list[str]:
        return []

    @override
    def all_files(self, directory: str) -> list[str]:
        return []

    @override
    def directories(self, directory: str) -> list[str]:
        return []

    @override
    def all_directories(self, directory: str) -> list[str]:
        return []

    @override
    def exists_directory(self, directory: str) -> bool:
        return False

    @override
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional[StorageDriver] = None
    ) -> bool:
        return False

    @override
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        return False

    @override
    def make_directory(self, directory: str) -> bool:
        return False

    @override
    def delete_directory(self, directory: str) -> bool:
        return False

    @override
    def rename_directory(self, source: str, target: str) -> bool:
        return False

    @override
    def get_metadata(self, path: str) -> Optional[Metadata]:
        return None

    @override
    def get_root(self) -> str:
        return ""

    @override
    def get_separator(self) -> DirectorySeparator:
        return self._separator
