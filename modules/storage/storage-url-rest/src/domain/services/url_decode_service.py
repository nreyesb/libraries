# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_decode_service.py
Author: Toku
"""
from overrides import override
from toku.storage.url.core import UrlMetadata
from src.domain.port.inbounds import UrlDecodeUseCase
from src.domain.port.outbounds import UrlDecodePort


class UrlDecodeService(UrlDecodeUseCase):
    """
    Provides the service for url decode.
    """

    def __init__(
            self,
            url_decode_port: UrlDecodePort
    ) -> None:
        """
        Initialize the url decode service.

        Args:
            url_decode_port (UrlDecodePort): The url decode port
        """
        self._url_decode_port: UrlDecodePort = url_decode_port

    @override
    def decode(self, metadata: str) -> UrlMetadata:
        return self._url_decode_port.decode(metadata)
