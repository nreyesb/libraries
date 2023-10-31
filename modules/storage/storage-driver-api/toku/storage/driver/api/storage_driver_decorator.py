# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: storage_driver_decorator.py
Author: Toku Dev
"""
from abc import ABC
from typing import Final, Type
from toku.storage.driver.api import StorageDriver


class StorageDriverDecorator(StorageDriver, ABC):
    """
    Abstract base class for storage driver decorators.
    """

    def __init__(self, storage_driver: StorageDriver) -> None:
        """
        Initialize the StorageDriverDecorator.

        Args:
            storage_driver (StorageDriver): The storage driver to be wrapped.
        """
        self._storage_driver: Final[StorageDriver] = storage_driver

    def get_storage_driver_reference(self) -> Type[StorageDriver]:
        """
        Get a reference to the wrapped storage driver class.

        Returns:
            Type[StorageDriver]: The class of the wrapped storage driver.
        """
        return type(self._storage_driver)
