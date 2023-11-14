# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url.py
Author: Toku
"""
from dataclasses import dataclass
from toku.storage.url.core import UrlSchema
from toku.storage.url.core import StorageUrlException


@dataclass
class Url:
    """
    Provides the abstraction of an URL.
    """

    schema: UrlSchema  # the schema type to get the resource
    authority: str  # the domain to get the resource, for example: www.my-domain.com
    path: str  # the endpoint path to get the resource, for example: streaming/get/{metadata}

    def to_url(self) -> str:
        """
        Creates the URL using `schema`, `authority` and `path`.

        For example:

        https://www.my-domain.com/path
        """
        if not self.authority.strip():
            raise StorageUrlException("authority can't be empty")

        if not self.path.strip():
            raise StorageUrlException("path can't be empty")

        return f"{self.schema.value}://" \
               f"{self.authority}" \
               f"/{self.path}"
