# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encode_repository.py
Author: Toku
"""
from overrides import override
from toku.storage.url.api import StorageUrl
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded
from src.domain.port.outbounds import UrlEncodePort


class UrlEncodeRepository(UrlEncodePort):
    """
    Provides the repository to encode an URL.
    """

    def __init__(
            self,
            storage_url: StorageUrl
    ) -> None:
        """
        Initialize the UrlEncodeRepository.

        Args:
            storage_url (StorageUrl): The storage url to encode the URL
        """
        self._storage_url: StorageUrl = storage_url

    @override
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> UrlEncoded:
        return self._storage_url.encode(url, url_metadata)
