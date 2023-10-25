# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
# flake8: noqa F401
"""
This package provides the StorageDriver API for testing purpose.

Classes:
    - StubStorageDriver (stub_storage_driver.py): Stub storage driver for testing purpose
    - PathSanitizerTests (path_sanitizer_tests.py): Path sanitizier tests for PathSanitizer
    - PathSanitizerStorageDriverDecoratorTests (path_sanitizer_storage_driver_decorator_tests.py): Path sanitizier storage driver decorator tests for PathSanitizerStorageDriverDecorator
    - StorageDriverTest (storage_driver_test.py): The contract for storage driver api testing
    - AbstractStorageDriverTest (abstract_storage_driver_test.py): Abstract storage driver tests for AbstractStorageDriver
"""
from .stub_storage_driver import StubStorageDriver as StubStorageDriver
from .path_sanitizer_tests import PathSanitizerTests as PathSanitizerTests
from .path_sanitizer_storage_driver_decorator_tests import PathSanitizerStorageDriverDecoratorTests as PathSanitizerStorageDriverDecoratorTests
from .storage_driver_test import StorageDriverTest as StorageDriverTest
from .abstract_storage_driver_test import AbstractStorageDriverTest as AbstractStorageDriverTest
