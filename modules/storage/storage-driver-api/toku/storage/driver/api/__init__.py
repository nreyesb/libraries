# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
# flake8: noqa F401
"""
This package provides the StorageDriver API.

Classes:
    - Status (storage_driver.py): The possible status of the driver
    - DirectorySeparator (storage_driver.py): The kinds of directory separator
    - Size (storage_driver.py): The size of a path
    - Metadata (storage_driver.py): The metadata of a path
    - PathSanitizer (path_sanitizer.py): The path sanitizer
    - StorageDriverException (storage_driver_exception.py): The storage driver exception
    - StorageDriver (storage_driver.py): The contract for storage driver process
    - AbstractStorageDriver (abstract_storage_driver.py): The default implementation for storage driver process
    - StorageDriverDecorator (storage_driver_decorator.py): The base for any storage driver decorator
    - PathSanitizerStorageDriverDecorator (path_sanitizer_storage_driver_decorator.py): The decorator for storage driver path sanitizier
    - OpenCloseStatusCheckerStorageDriverDecorator (open_close_status_checker_storage_driver_decorator.py): The decorator for storage driver open / close checker
"""
from .storage_driver import Status as Status
from .storage_driver import DirectorySeparator as DirectorySeparator
from .storage_driver import Size as Size
from .storage_driver import Metadata as Metadata
from .path_sanitizer import PathSanitizer as PathSanitizer
from .storage_driver_exception import StorageDriverException as StorageDriverException
from .storage_driver import StorageDriver as StorageDriver
from .abstract_storage_driver import AbstractStorageDriver as AbstractStorageDriver
from .storage_driver_decorator import StorageDriverDecorator as StorageDriverDecorator
from .path_sanitizer_storage_driver_decorator import PathSanitizerStorageDriverDecorator as PathSanitizerStorageDriverDecorator
from .open_close_status_checker_storage_driver_decorator import OpenCloseStatusCheckerStorageDriverDecorator as OpenCloseStatusCheckerStorageDriverDecorator
