# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_streaming_service.py
Author: Toku
"""
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlStreaming
from src.domain.port.inbounds import UrlStreamingUseCase
from src.domain.port.outbounds import UrlDecodePort
from src.domain.port.outbounds import UrlStreamingPort


class UrlStreamingService(UrlStreamingUseCase):
    """
    Provides the service for url streaming.
    """

    def __init__(
            self,
            url_decode_port: UrlDecodePort,
            url_streaming_port: UrlStreamingPort
    ) -> None:
        """
        Initialize the url streaming service.

        Args:
            url_decode_port (UrlDecodePort): The url decode port
            url_streaming_port (UrlStreamingPort): The url streming port
        """
        self._url_decode_port: UrlDecodePort = url_decode_port
        self._url_streaming_port: UrlStreamingPort = url_streaming_port

    @override
    def streaming(self, metadata: str) -> UrlStreaming:
        url_metadata: UrlMetadata = self._url_decode_port.decode(metadata)
        return self._url_streaming_port.streaming(url_metadata)
