# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_driver_factory.py
Author: Toku
"""
from typing import Optional
from overrides import override
from toku.storage.driver.api import StorageDriver
from src.common.creator import Creator
from src.common.factory import Factory
from src.infrastructure.creators import VccVoucherStorageDriverCreator


class StorageDriverFactory(Factory[StorageDriver]):
    """
    The StorageDriverFactory implementation.

    It uses the following creators:

    - VCC-VOUCHER = VccVoucherStorageDriverCreator
    """

    _CREATOR: dict[str, Creator[StorageDriver]] = {
        "VCC-VOUCHER": VccVoucherStorageDriverCreator()
    }

    @override
    def create(self, reference: str) -> StorageDriver:
        creator: Optional[Creator[StorageDriver]] = StorageDriverFactory._CREATOR.get(reference)

        if creator:
            return creator.create()

        raise ValueError(f"reference '{reference}' to create the storage driver is not valid")
