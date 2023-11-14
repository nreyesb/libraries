# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: vcc_voucher_storage_driver_creator.py
Author: Toku
"""
import os
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.gcs import GcsStorageDriver
from src.common.creator import Creator


class VccVoucherStorageDriverCreator(Creator[StorageDriver]):
    """
    The VccVoucherStorageDriverCreator implementation.

    Creates a GcsStorageDriver.
    """

    @override
    def create(self) -> StorageDriver:
        return GcsStorageDriver(
            root=os.getenv("STORAGE_URL_VCC_GCS_VOUCHER_ROOT", ""),
            project_id=os.getenv("STORAGE_URL_GCS_VCC_VOUCHER_PROJECT_ID", ""),
            bucket_name=os.getenv("STORAGE_URL_GCS_VCC_VOUCHER_BUCKET_NAME", "")
        )
