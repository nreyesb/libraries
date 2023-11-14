# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encode_port.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded


class UrlEncodePort(ABC, EnforceOverrides):
    """
    Provides the port to encode a metadata generating an URL to get
    a resource.
    """

    @abstractmethod
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> UrlEncoded:
        """
        Provides the process to create the `UrlEncoded` based on the `Url` and
        `UrlMetadata` reported.

        Args:
            url (Url): The url
            url_metadata (UrlMetada): The url metadata

        Returns:
            UrlEncoded: The url encoded
        """
