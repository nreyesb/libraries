# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_url_factory.py
Author: Toku
"""
from typing import Optional
from overrides import override
from toku.storage.url.api import StorageUrl
from src.common.creator import Creator
from src.common.factory import Factory
from src.infrastructure.creators import BuiltInMetadataStorageUrlCreator


class StorageUrlFactory(Factory[StorageUrl]):
    """X
    The StorageUrlFactory implementation.

    It uses the following creators:

    - BUILT-IN = BuiltInMetadataStorageUrlCreator
    """

    _CREATOR: dict[str, Creator[StorageUrl]] = {
        "BUILT-IN": BuiltInMetadataStorageUrlCreator()
    }

    @override
    def create(self, reference: str) -> StorageUrl:
        creator: Optional[Creator[StorageUrl]] = StorageUrlFactory._CREATOR.get(reference)

        if creator:
            return creator.create()

        raise ValueError(f"reference '{reference}' to create the storage url is not valid")
