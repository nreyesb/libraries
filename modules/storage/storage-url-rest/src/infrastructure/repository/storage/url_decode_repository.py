# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_decode_repository.py
Author: Toku
"""
from overrides import override
from toku.storage.url.api import StorageUrl
from toku.storage.url.core import UrlMetadata
from src.domain.port.outbounds import UrlDecodePort


class UrlDecodeRepository(UrlDecodePort):
    """
    Provides the repository to decode an URL.
    """

    def __init__(
        self,
        storage_url: StorageUrl
    ) -> None:
        """
        Initialize the UrlDecodeRepository.

        Args:
            storage_url (StorageUrl): The storage url to decode the URL
        """
        self._storage_url: StorageUrl = storage_url

    @override
    def decode(self, metadata: str) -> UrlMetadata:
        return self._storage_url.decode(metadata)
