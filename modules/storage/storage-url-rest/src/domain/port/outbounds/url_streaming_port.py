# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_streaming_port.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlStreaming


class UrlStreamingPort(ABC, EnforceOverrides):
    """
    Provides the port to streaming an `UrlMetadata` to return the
    input stream that represents the resource.
    """

    @abstractmethod
    def streaming(self, url_metadata: UrlMetadata) -> UrlStreaming:
        """
        Provides the process to get the resource of the `url_metadata`
        as input stream.

        Args:
            url_metadata (UrlMetadata): The url metadata

        Returns:
            UrlStreaming: The url streaming
        """
