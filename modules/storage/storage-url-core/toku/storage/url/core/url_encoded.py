# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encoded.py
Author: Toku
"""
from dataclasses import dataclass
from toku.storage.url.core import Url
from toku.storage.url.core import StorageUrlException


@dataclass
class UrlEncoded(Url):
    """
    Provides the data for an encoded url that allows to get a resource.

    The `metadata` attribute is the metadata as string, it should be a string
    representation of `UrlMetadata`.
    """

    metadata: str  # the encoded metadata, for example: hj9sa7d8fags9ad876fas9587duyasfdjhf

    def to_url(self) -> str:
        """
        Creates the URL to get the resource using the `super().to_url()` and
        replacing the string {metadata} in the `path` with the `metadata`
        itself.

        For example:

        raw = https://www.my-domain.com/streaming/get/{metadata}
        url = https://www.my-domain.com/streaming/get/hj9sa7d8fags9ad876fas9587duyasfdjhf
        """
        url: str = super().to_url()

        if not self.metadata.strip():
            raise StorageUrlException("metadata can't be empty")

        return f"{url.replace('{metadata}', self.metadata)}"
