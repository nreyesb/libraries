# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_streaming_use_case.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.url.core import UrlStreaming


class UrlStreamingUseCase(ABC, EnforceOverrides):
    """
    Provides the UseCase to streaming a metadata as string to return the
    input stream that represents the resource.
    """

    @abstractmethod
    def streaming(self, metadata: str) -> UrlStreaming:
        """
        Provides the process to get the resource of the `metadata`
        as input stream.

        Args:
            metadata (str): The metadata as string

        Returns:
            UrlStreaming: The url streaming
        """
