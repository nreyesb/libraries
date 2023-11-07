# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_encoded.py
Author: Toku Dev
"""
from dataclasses import dataclass
from toku.storage.url.core import UrlSchema
from toku.storage.url.core import StorageUrlException


@dataclass
class UrlEncoded:
    """
    Provides the data for an encoded url that allows to get a resource.

    The `metadata` attribute is the metadata as string, it should be a string
    representation of `UrlMetadata`.
    """

    schema: UrlSchema  # the schema type to get the resource
    authority: str  # the domain to get the resource, for example: www.my-domain.com
    path: str  # the endpoint path to get the resource, for example: streaming/get/{metadata}
    metadata: str  # the encoded metadata, for example: hj9sa7d8fags9ad876fas9587duyasfdjhf

    def to_url(self) -> str:
        """
        Creates the URL to get the resource using `schema`, `authority` and `path`
        where the string {metadata} in `path` is replaced by the `metadata` itself.

        For example:

        https://www.my-domain.com/streaming/get/hj9sa7d8fags9ad876fas9587duyasfdjhf
        """
        if not self.authority.strip():
            raise StorageUrlException("authority can't be empty")

        if not self.path.strip():
            raise StorageUrlException("path can't be empty")

        if not self.metadata.strip():
            raise StorageUrlException("metadata can't be empty")

        return f"{self.schema.value}://" \
               f"{self.authority}" \
               f"/{self.path.replace('{metadata}', self.metadata)}"
