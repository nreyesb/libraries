# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_decode_use_case.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.url.core import UrlMetadata


class UrlDecodeUseCase(ABC, EnforceOverrides):
    """
    Provides the UseCase to decode a metadata as string to get the original
    information that allows to get a resource.
    """

    @abstractmethod
    def decode(self, metadata: str) -> UrlMetadata:
        """
        Provides the process to create the `UrlMetadata` based on the `metadata`.

        Args:
            metadata (str): The metadata as string

        Returns:
            UrlMetadata: The url metadata
        """
