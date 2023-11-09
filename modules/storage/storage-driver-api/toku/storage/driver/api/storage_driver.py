# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_driver.py
Author: Toku
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Literal, Optional, Self, final, overload
from io import BufferedReader
from dataclasses import dataclass
import mimetypes
from overrides import EnforceOverrides
import humanize


class Status(Enum):
    """
    Provides the possibles status values for the storage driver.
    """

    NOT_OPENED = "NOT_OPENED"
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class DirectorySeparator(Enum):
    """
    Provides the diferrents kinds of directory separator for paths
    """

    SLASH = "/"
    BACKSLASH = "\\"


@dataclass
class Size:
    """
    Provides the size of a file and the converter to human-readable.
    """

    length: int  # the length of a file in bytes
    human_readable: str  # the length as human readable format

    def __init__(self, length: int) -> None:
        """
        Convert the 'length' to a human redeable str with humanize.
        """
        self.length = length
        self.human_readable: str = humanize.naturalsize(length)


@dataclass
class Metadata:
    """
    Provides the metadata of an element.
    """

    size: Size
    creation_time: int  # the creatime time date as integer
    last_modified: int  # the last modified date as integer
    last_access_time: int  # the last access date as integer
    is_file: bool  # indicates if it's a file
    is_directory: bool  # indicates if it's a directory
    is_symbolic_link: bool  # indicates if it's a symbolik link
    media_type: str  # the media type of the file

    @staticmethod
    def detect_media_type(path: str) -> str:
        """
        Detect media type.

        Try to detect the media type via mimetypes.guess_type(path).

        Args:
            path (str): The path.

        Returns:
            str: The media type.
        """
        media_type, _ = mimetypes.guess_type(path)
        return "" if not media_type else media_type


class StorageDriver(ABC, EnforceOverrides):
    """
    Provides the contract to define the abstraction to use the storage driver.

    Consider the following as part of the specification:

    - The root returned with `get_root()` is the working directory where each file
      and directory have to be.
    - The separator returned with `get_separator()` is to indicate how the directories
      are separated.
    - The `open()` and `close()` method are to initialize and release the resources
      of the storage driver.

    Consider the following as not part of the specification but highly recommended:

    - Each file or directory passed as an argument or obtained from a method has
      to be consistent with the separator.
    - Each method should consider the status of the storage driver based on it's
      opended or closed.

    For the previous conditions check the decorators:

    - PathSanitizerStorageDriverDecorator
    - OpenCloseStatusCheckerStorageDriverDecorator
    """

    @abstractmethod
    def open(self) -> None:
        """
        Allows storage driver initialization.
        """

    @abstractmethod
    def close(self) -> None:
        """
        Closes the storage driver and releases its resources.
        """

    @abstractmethod
    def get(self, file: str) -> Optional[bytes]:
        """
        Gets `file` as a byte array.

        If `file` doesn't exist, return None.

        Args:
            file (str): Full file path.

        Returns:
            Optional[bytes]: Byte array or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def get_as_input_stream(self, file: str) -> Optional[BufferedReader]:
        """
        Gets `file` as an input stream.

        If `file` doesn't exist, return None.

        Args:
            file (str): Full file path.

        Returns:
            Optional[BufferedReader]: Input stream or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def exists(self, file: str) -> bool:
        """
        Checks if `file` exists.

        Args:
            file (str): Full file path.

        Returns:
            bool: True if the file exists, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file(self, source: bytes, directory: str) -> Optional[str]:
        """
        Stores the `source` into `directory`.

        If `directory` is empty or None, use the root as a directory.
        If `directory` is a file, the process is finished. Filename is auto-generated.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (bytes): Content as a byte array.
            directory (str): Directory to store the content. Defaults to None.

        Returns:
            Optional[str]: Filename or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file(self, source: str, directory: str) -> Optional[str]:
        """
        Stores the `source` into `directory`.

        If `directory` is empty or None, use the root as a directory.
        If `directory` is a file, the process is finished. Filename is auto-generated.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (str): Full file path
            directory (str): Directory to store the content. Defaults to None.

        Returns:
            Optional[str]: Filename or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file(self, source: BufferedReader, directory: str) -> Optional[str]:
        """
        Stores the `source` into `directory`.

        If `directory` is empty or None, use the root as a directory.
        If `directory` is a file, the process is finished. Filename is auto-generated.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (BufferedReader): Content as an input stream
            directory (str): Directory to store the content. Defaults to None.

        Returns:
            Optional[str]: Filename or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def put_file(self, source: bytes | str | BufferedReader, directory: str) -> Optional[str]:
        """
        Stores the `source` into `directory`.

        If `directory` is empty or None, use the root as a directory.
        If `directory` is a file, the process is finished. Filename is auto-generated.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (bytes | str | BufferedReader): Content.
            directory (str): Directory to store the content. Defaults to None.

        Returns:
            Optional[str]: Filename or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file_as(self, source: bytes, file: str) -> bool:
        """
        Stores the `source` into `file`.

        If `source` is None, the process is finished.
        If `file` is empty, None, or a directory, or the parent folder is a file,
        the process is finished.
        If `file` exists, it'll be replaced.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (bytes): Content as a byte array.
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file_as(self, source: str, file: str) -> bool:
        """
        Stores the `source` into `file`.

        If `source` is None, the process is finished.
        If `file` is empty, None, or a directory, or the parent folder is a file,
        the process is finished.
        If `file` exists, it'll be replaced.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (str): Full file path
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def put_file_as(self, source: BufferedReader, file: str) -> bool:
        """
        Stores the `source` into `file`.

        If `source` is None, the process is finished.
        If `file` is empty, None, or a directory, or the parent folder is a file,
        the process is finished.
        If `file` exists, it'll be replaced.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (BufferedReader): Content as an input stream
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def put_file_as(self, source: bytes | str | BufferedReader, file: str) -> bool:
        """
        Stores the `source` into `file`.

        If `source` is None, the process is finished.
        If `file` is empty, None, or a directory, or the parent folder is a file,
        the process is finished.
        If `file` exists, it'll be replaced.
        If the parent directory doesn't exist, it'll be created, and if it can't
        be created, the process is finished.

        Args:
            source (bytes | str | BufferedReader): Content
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def append(self, source: bytes, file: str) -> bool:
        """
        Adds the `source` to the end of `file`.

        If `source` is None, the process is finished.
        If `file` is empty, None, a directory, or doesn't exist, the process is finished.

        Args:
            source (bytes): Content as a byte array.
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def copy(self, source: str, target: str) -> bool:
        """
        Copies the `source` into `target` using the current storage driver.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def copy(self, source: str, target: str, target_storage_driver: 'StorageDriver') -> bool:
        """
        Copies the `source` into `target` using the `target_storage_driver` in the target.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            target_storage_driver (StoragaDriver): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def copy(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        """
        Copies the `source` into `target` using the `target_storage_driver` in the target.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            target_storage_driver (Optional[StorageDriver]): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def move(self, source: str, target: str) -> bool:
        """
        Moves the `source` to `target` using the current storage driver.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def move(self, source: str, target: str, target_storage_driver: 'StorageDriver') -> bool:
        """
        Moves the `source` to `target` using the `target_storage_driver` in the target.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            target_storage_driver (StoragaDriver): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def move(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        """
        Moves the `source` to `target` using the `target_storage_driver` in the target.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` is empty or a directory, return False.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full file path.
            target (str): Full file path.
            target_storage_driver (Optional[StorageDriver]): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def delete(self, file: str) -> bool:
        """
        Deletes `file`.

        If `file` doesn't exist or is a directory, return False.

        Args:
            file (str): Full file path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def rename(self, source: str, target: str) -> bool:
        """
        Renames the `source` to `target`.

        If `source` doesn't exist or is a directory, return False.
        If `source` exists and `target` is the same, return False.
        If `target` exists or is a directory, return False.

        The difference between rename and move is that rename simply changes the path
        of the file without performing any operations.

        Args:
            source (str): Full file path.
            target (str): Full file path.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def files(self, directory: str) -> list[str]:
        """
        Returns a collection with all the files inside the root of the `directory`.

        If `directory` doesn't exist or is a file, return an empty list.
        If `directory` is empty or None, use the root as a directory.
        If the process can't access the files, return an empty list.

        Args:
            directory (str): Full directory path. Defaults to None.

        Returns:
            list[str]: List of file paths.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def all_files(self, directory: str) -> list[str]:
        """
        Returns a collection with all the files inside the root and sub-directories
        of the `directory`, where each file has the full path without the root.

        If `directory` doesn't exist or is a file, return an empty collection.
        If `directory` is empty or None, use the root as a directory.

        Args:
            directory (str): Directory to use to get the files.

        Returns:
            list[str]: All the files inside the root and sub-directories of the directory.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def directories(self, directory: str) -> list[str]:
        """
        Returns a collection with all the directories inside the root of the `directory`.

        If `directory` doesn't exist or is a file, return an empty list.
        If `directory` is empty or None, use the root as a directory.
        If the process can't access the directories, return an empty list.

        Args:
            directory (str): Full directory path. Defaults to None.

        Returns:
            list[str]: List of directory paths.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def all_directories(self, directory: str) -> list[str]:
        """
        Returns a collection with all the directories inside the root and
        sub-directories of the `directory`, where each directory has the full path
        without the root.

        If `directory` doesn't exist or is a file, return an empty collection.
        If `directory` is empty or None, use the root as a directory.

        Args:
            directory (str): Directory to use to get the directories.

        Returns:
            list[str]: All the directories inside the root and sub-directories of the
            directory.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def exists_directory(self, directory: str) -> bool:
        """
        Checks if `directory` exists.

        Args:
            directory (str): Full directory path.

        Returns:
            bool: True if the directory exists, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @overload
    def copy_directory(self, source: str, target: str) -> bool:
        """
        Copy the 'source' into 'target' using the current storage driver.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @overload
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: 'StorageDriver'
    ) -> bool:
        """
        Copy the 'source' into 'target' using the 'target_storage_driver' in the target.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.
            target_storage_driver (StoragaDriver): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @abstractmethod
    def copy_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        """
        Copy the 'source' into 'target' using the 'target_storage_driver' in the target.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.
            target_storage_driver (Optional[StorageDriver]): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @overload
    def move_directory(self, source: str, target: str) -> bool:
        """
        Move the 'source' into 'target' using the current storage driver.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @overload
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: 'StorageDriver'
    ) -> bool:
        """
        Move the 'source' into 'target' using the 'target_storage_driver' in the target.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.
            target_storage_driver: Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @abstractmethod
    def move_directory(
        self,
        source: str,
        target: str,
        target_storage_driver: Optional['StorageDriver'] = None
    ) -> bool:
        """
        Move the 'source' into 'target' using the 'target_storage_driver' in the target.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.
            target_storage_driver (Optional[StorageDriver]): Storage driver to use in the target.

        Returns:
            bool: True if the action could be executed.

        Raises:
            StorageDriverException: If there's an issue with the storage driver.
        """

    @abstractmethod
    def make_directory(self, directory: str) -> bool:
        """
        Creates a `directory`.

        If `directory` is empty, None, or exists, the process is finished.

        Args:
            directory (str): Full directory path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def delete_directory(self, directory: str) -> bool:
        """
        Deletes `directory`.

        If `directory` doesn't exist, return False.
        If `directory` is a file or isn't empty, the process is finished.

        Args:
            directory (str): Full directory path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def rename_directory(self, source: str, target: str) -> bool:
        """
        Renames `source` into `target`.

        If `source` doesn't exist, is a file, or is the same as `target`, return False.
        If `target` is empty or a directory, the process is finished.
        If `target` already exists, it'll be replaced.

        Args:
            source (str): Full directory path.
            target (str): Full directory path.

        Returns:
            bool: True if the action could be executed, False otherwise.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def get_metadata(self, path: str) -> Optional[Metadata]:
        """
        Gets the metadata of `path`.

        If `path` doesn't exist, return None.

        Args:
            path (str): Full file or directory path.

        Returns:
            Optional[Metadata]: Metadata or None.

        Raises:
            StorageDriverException: If a storage driver exception occurs.
        """

    @abstractmethod
    def get_root(self) -> str:
        """
        Returns the root directory of the storage driver.

        Returns:
            str: Root directory path.
        """

    @abstractmethod
    def get_separator(self) -> DirectorySeparator:
        """
        Returns the directory separator used by the storage driver.

        Returns:
            DirectorySeparator: Directory separator.
        """

    @final
    def __enter__(self) -> Self:
        self.open()
        return self

    @final
    def __exit__(self, exc_type_: Any, exc_value_: Any, traceback_: Any) -> Literal[False]:
        self.close()
        return False  # indicates that exceptions should be propagated
