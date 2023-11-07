# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_url_decorator.py
Author: Toku Dev
"""
from abc import ABC
from typing import Final, Type
from toku.storage.url.api import StorageUrl


class StorageUrlDecorator(StorageUrl, ABC):
    """
    Abstract base class for storage url decorators.
    """

    def __init__(self, storage_url: StorageUrl) -> None:
        """
        Initialize the StorageUrlDecorator.

        Args:
            storage_url (StorageUrl): The storage url to be wrapped.
        """
        self._storage_url: Final[StorageUrl] = storage_url

    def get_storage_url_reference(self) -> Type[StorageUrl]:
        """
        Get a reference to the wrapped storage url class.

        Returns:
            Type[StorageUrl]: The class of the wrapped storage url.
        """
        return type(self._storage_url)
