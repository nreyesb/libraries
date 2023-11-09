# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: open_close_status_checker_storage_driver_decorator.py
Author: Toku
"""
from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Optional, final
from overrides import override
from toku.storage.driver.api import Status
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.api import StorageDriverException
from toku.storage.driver.api import StorageDriverDecorator


class StatusHandler(ABC):
    """
    Base class for managing the storage driver status.
    """

    def __init__(self, storage_driver: 'OpenCloseStatusCheckerStorageDriverDecorator') -> None:
        """
        Initializes a new StatusHandler.

        Args:
            storage_driver: The associated storage driver.
        """
        self._storage_driver: 'OpenCloseStatusCheckerStorageDriverDecorator' = storage_driver

    def check_status(self, must_have_status: 'StatusHandler') -> None:
        """
        Checks if the reported status is equal to the internal status.

        Args:
            must_have_status (StatusHandler): The status that the internal storage must have.

        Raises:
            StorageDriverException: If the statuses do not match.
        """
        if str(must_have_status) != str(self):
            raise StorageDriverException(
                f"Storage driver status is {self} and must be {must_have_status}"
                "to execute the action"
            )

    @abstractmethod
    def handle_request(self) -> None:
        """
        Change the status on the storage driver.
        """


class NotOpenedStatusHandler(StatusHandler):
    """
    StatusHandler for the 'NOT_OPENED' status.
    """

    @override
    def handle_request(self) -> None:
        """
        Changes the status to 'OPENED'.
        """
        self._storage_driver.status_handler = self._storage_driver.opened_status_handler

    def __str__(self) -> str:
        return Status.NOT_OPENED.name


class OpenedStatusHandler(StatusHandler):
    """
    StatusHandler for the 'OPENED' status.
    """

    @override
    def handle_request(self) -> None:
        """
        Changes the status to 'CLOSED'.
        """
        self._storage_driver.status_handler = self._storage_driver.closed_status_handler

    def __str__(self) -> str:
        return Status.OPENED.name


class ClosedStatusHandler(StatusHandler):
    """
    StatusHandler for the 'CLOSED' status.
    """

    @override
    def handle_request(self) -> None:
        """
        Throws an exception because it's not possible to execute an action on a closed
        storage driver.
        """
        raise StorageDriverException(f"Storage driver status is {self}, it can't be changed")

    def __str__(self) -> str:
        return Status.CLOSED.name


@final
class OpenCloseStatusCheckerStorageDriverDecorator(StorageDriverDecorator):
    """
    Provides a decorator to wrap the Status enum and ensure that each
    method has the correct status to be invoked.
    """

    def __init__(self, storage_driver: StorageDriver) -> None:
        """
        Initializes a new OpenCloseStatusCheckerStorageDriverDecorator.

        Args:
            storage_driver (StorageDriver): The storage driver to decorate.
        """
        super().__init__(storage_driver)
        self.not_opened_status_handler: StatusHandler = NotOpenedStatusHandler(self)
        self.opened_status_handler: StatusHandler = OpenedStatusHandler(self)
        self.closed_status_handler: StatusHandler = ClosedStatusHandler(self)
        self.status_handler: StatusHandler = self.not_opened_status_handler

    @override
    def open(self) -> None:
        self.status_handler.check_status(self.not_opened_status_handler)

        try:
            self._storage_driver.open()
        finally:
            self.status_handler.handle_request()

    @override
    def close(self) -> None:
        self.status_handler.check_status(self.opened_status_handler)

        try:
            self._storage_driver.close()
        finally:
            self.status_handler.handle_request()

    @override
    def get(self, file: str) -> Optional[bytes]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.get(file)

    @override
    def get_as_input_stream(self, file: str) -> Optional[BufferedReader]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.get_as_input_stream(file)

    @override
    def exists(self, file: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.exists(file)

    @override
    def put_file(self, source: bytes | str | BufferedReader, directory: str) -> Optional[str]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.put_file(source, directory)

    @override
    def put_file_as(self, source: bytes | str | BufferedReader, file: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.put_file_as(source, file)

    @override
    def append(self, source: bytes, file: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.append(source, file)

    @override
    def copy(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        self.status_handler.check_status(self.opened_status_handler)

        if not target_storage_driver:
            return self._storage_driver.copy(source, target)

        return self._storage_driver.copy(source, target, target_storage_driver)

    @override
    def move(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        self.status_handler.check_status(self.opened_status_handler)

        if not target_storage_driver:
            return self._storage_driver.move(source, target)

        return self._storage_driver.move(source, target, target_storage_driver)

    @override
    def delete(self, file: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.delete(file)

    @override
    def rename(self, source: str, target: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.rename(source, target)

    @override
    def files(self, directory: str) -> list[str]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.files(directory)

    @override
    def all_files(self, directory: str) -> list[str]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.all_files(directory)

    @override
    def directories(self, directory: str) -> list[str]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.directories(directory)

    @override
    def all_directories(self, directory: str) -> list[str]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.all_directories(directory)

    @override
    def exists_directory(self, directory: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.exists_directory(directory)

    @override
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        self.status_handler.check_status(self.opened_status_handler)

        if not target_storage_driver:
            return self._storage_driver.copy_directory(source, target)

        return self._storage_driver.copy_directory(source, target, target_storage_driver)

    @override
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        if not target_storage_driver:
            return self._storage_driver.move_directory(source, target)

        return self._storage_driver.move_directory(source, target, target_storage_driver)

    @override
    def make_directory(self, directory: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.make_directory(directory)

    @override
    def delete_directory(self, directory: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.delete_directory(directory)

    @override
    def rename_directory(self, source: str, target: str) -> bool:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.rename_directory(source, target)

    @override
    def get_metadata(self, path: str) -> Optional[Metadata]:
        self.status_handler.check_status(self.opened_status_handler)
        return self._storage_driver.get_metadata(path)

    @override
    def get_root(self) -> str:
        return self._storage_driver.get_root()

    @override
    def get_separator(self) -> DirectorySeparator:
        return self._storage_driver.get_separator()

    def get_status(self) -> Status:
        """
        Gets the status.

        Returns:
            str: The status.
        """
        return Status(str(self.status_handler))
