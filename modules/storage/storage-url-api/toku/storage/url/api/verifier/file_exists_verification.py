# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: file_exists_verification.py
Author: Toku
"""
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.url.api.verifier import ConflictStorageUrlVerificationException
from toku.storage.url.core import UrlMetadata
from toku.storage.url.verifier.api import Verification


class FileExistsVerification(Verification):
    """
    Performs a verification to see if the path exists on the storage driver.
    """

    def __init__(self, storage_driver: StorageDriver) -> None:
        """
        Create a new file exists verification.

        Args:
            storage_driver (StorageDriver): The storage driver
        """
        self._storage_driver: StorageDriver = storage_driver

    @override
    def verify(self, url_metadata: UrlMetadata) -> None:
        """
        Checks if the path in the `url_metadata` exists in the `self._storage_driver`.

        Args:
            url_metadata (UrlMetadata): The url metadata

        Raises:
            StorageUrlVerificationException: Problem with validation integrity
        """
        if not self._storage_driver.exists(url_metadata.path):
            raise ConflictStorageUrlVerificationException(
                f"file {url_metadata.path} doesn't exists"
            )
