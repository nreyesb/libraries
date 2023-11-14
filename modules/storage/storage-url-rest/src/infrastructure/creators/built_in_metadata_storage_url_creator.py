# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: built_in_metadata_storage_url_creator.py
Author: Toku
"""
import os
from overrides import override
from toku.storage.url.api import StorageUrl
from toku.storage.url.built_in import BuiltInMetadataStorageUrl
from src.common.creator import Creator


class BuiltInMetadataStorageUrlCreator(Creator[StorageUrl]):
    """
    The BuiltInMetadataStorageUrlCreator implementation.

    Creates a BuiltInMetadataStorageUrl.
    """

    @override
    def create(self) -> StorageUrl:
        return BuiltInMetadataStorageUrl(
            bytes(os.getenv("STORAGE_URL_SECRET_KEY", ""), "UTF-8")
        )
