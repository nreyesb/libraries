# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encode_service.py
Author: Toku
"""
from overrides import override
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata
from src.domain.port.inbounds import UrlEncodeUseCase
from src.domain.port.outbounds import UrlEncodePort


class UrlEncodeService(UrlEncodeUseCase):
    """
    Provides the service for url encode.
    """

    def __init__(
            self,
            url_encode_port: UrlEncodePort
    ) -> None:
        """
        Initialize the url encode service.

        Args:
            url_encode_port (UrlEncodePort): The url encode port
        """
        self._url_encode_port: UrlEncodePort = url_encode_port

    @override
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> str:
        return self._url_encode_port.encode(url, url_metadata).to_url()
