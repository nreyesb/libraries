# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encode_use_case.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata


class UrlEncodeUseCase(ABC, EnforceOverrides):
    """
    Provides the UseCase to encode a metadata generating an URL to get
    a resource.
    """

    @abstractmethod
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> str:
        """
        Provides the process to create the URL as string based on the
        `Url` and `UrlMetadata` reported.

        Args:
            url (Url): The url
            url_metadata (UrlMetada): The url metadata

        Returns:
            str: The url
        """
