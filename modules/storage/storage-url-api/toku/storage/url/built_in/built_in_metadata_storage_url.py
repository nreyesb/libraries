# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: built_in_metadata_storage_url.py
Author: Toku
"""
import pickle
import base64
from typing import final
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.api import AbstractStorageUrl


class BuiltInMetadataStorageUrl(AbstractStorageUrl):
    """
    The `BuiltInMetadataStorageUrl` class provides an implementation where the
    `url_metadata` itself is contained in the path of the URL.
    """

    @final
    @override
    def _process_url_metadata(self, url_metadata: UrlMetadata) -> str:
        # convert the url metadata to bytes
        # convert the bytes to base64 url safe
        # decode the base64 url safe to string in UTF-8
        url_metadata_as_bytes: bytes = pickle.dumps(url_metadata)
        url_metadata_as_bytes = base64.urlsafe_b64encode(url_metadata_as_bytes)
        return url_metadata_as_bytes.decode('utf-8')

    @final
    @override
    def _process_metadata(self, metadata: str) -> UrlMetadata:
        # encode the string in UTF-8 to bytes
        # convert the base64 url safe to bytes
        # convert the bytes to url metadata
        metadata_as_bytes: bytes = metadata.encode('utf-8')
        metadata_as_bytes = base64.urlsafe_b64decode(metadata_as_bytes)
        return pickle.loads(metadata_as_bytes)  # type: ignore[no-any-return]
