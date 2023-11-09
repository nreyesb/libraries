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
from typing import Final, final
from overrides import override
from toku.crypto.cipher.api import Cipher
from toku.crypto.cipher.aes import AesCipher
from toku.storage.url.core import UrlMetadata
from toku.storage.url.api import AbstractStorageUrl


@final
class BuiltInMetadataStorageUrl(AbstractStorageUrl):
    """
    The `BuiltInMetadataStorageUrl` class provides an implementation where the
    `url_metadata` itself is contained in the path of the URL.
    """

    _DEFAULT_ENCODING: Final[str] = "UTF-8"

    def __init__(self, key: bytes) -> None:
        """
        Creates a new built-in metadara storage url.

        Args:
            key (bytes): The secret for aes cipher
        """
        self._cipher: Cipher = AesCipher(key)

    @override
    def _process_url_metadata(self, url_metadata: UrlMetadata) -> str:
        # convert the url metadata to bytes
        # encrypt the bytes
        # convert the bytes to base64 url safe
        # decode the base64 url safe to string in UTF-8
        url_metadata_as_bytes: bytes = pickle.dumps(url_metadata)
        url_metadata_as_bytes = self._cipher.encrypt(url_metadata_as_bytes)
        url_metadata_as_bytes = base64.urlsafe_b64encode(url_metadata_as_bytes)
        return url_metadata_as_bytes.decode(BuiltInMetadataStorageUrl._DEFAULT_ENCODING)

    @override
    def _process_metadata(self, metadata: str) -> UrlMetadata:
        # encode the string in UTF-8 to bytes
        # convert the base64 url safe to bytes
        # decrypt the bytes
        # convert the bytes to url metadata
        metadata_as_bytes: bytes = metadata.encode(BuiltInMetadataStorageUrl._DEFAULT_ENCODING)
        metadata_as_bytes = base64.urlsafe_b64decode(metadata_as_bytes)
        metadata_as_bytes = self._cipher.decrypt(metadata_as_bytes)
        return pickle.loads(metadata_as_bytes)  # type: ignore[no-any-return]
