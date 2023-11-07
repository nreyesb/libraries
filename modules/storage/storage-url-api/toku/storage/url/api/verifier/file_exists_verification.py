# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: verification.py
Author: Toku Dev
"""
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.url.core import UrlMetadata
from toku.storage.url.verifier import Verification
from toku.storage.url.verifier import StorageUrlVerificationException


class FileExistsVerification(Verification):
    """
    Perform a verification to see if the path exists on the storage driver.
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
        if not self._storage_driver.exists(url_metadata.path):
            raise StorageUrlVerificationException(f"file {url_metadata.path} doesn't exists")
