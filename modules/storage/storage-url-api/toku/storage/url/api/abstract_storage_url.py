# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: abstract_storage_url.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Optional, final
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.api import Metadata
from toku.storage.url.core import UrlSchema
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded
from toku.storage.url.core import UrlStreaming
from toku.storage.url.core import StorageUrlException
from toku.storage.url.verifier import Verification
from toku.storage.url.api import StorageUrl
from toku.storage.url.api.verifier import FileExistsVerification


class AbstractStorageUrl(StorageUrl, ABC):
    """
    The `AbstractStorageUrl` class provides a base for working with storage url.
    """

    def __init__(self, storage_driver: StorageDriver) -> None:
        """
        Initializes a new abstract storage driver.

        Args:
            storage_driver (StorageDriver): The storage driver.
        """
        self._storage_driver: StorageDriver = storage_driver

    @final
    @override
    def encode(
        self,
        schema: UrlSchema,
        authority: str,
        path: str,
        url_metadata: UrlMetadata
    ) -> UrlEncoded:
        # check if file exists
        # process url_metadata to get a string and check if it's not empry
        FileExistsVerification(self._storage_driver).verify(url_metadata)

        metadata: str = self._process_url_metadata(url_metadata)

        if not metadata.strip():
            raise StorageUrlException("url_metadata process is empty")

        return UrlEncoded(
            schema,
            authority,
            path,
            metadata
        )

    @final
    @override
    def decode(self, metadata: str) -> UrlMetadata:
        return self._process_metadata(metadata)

    @final
    @override
    def streaming(
        self,
        url_metadata: UrlMetadata,
        verifications: Optional[list[Verification]] = None
    ) -> UrlStreaming:
        # apply verifications
        FileExistsVerification(self._storage_driver).verify(url_metadata)

        if verifications:
            for verification in verifications:
                verification.verify(url_metadata)

        # TODO: apply internal verifications

        # create url streaming
        input_stream: Optional[BufferedReader] = self._storage_driver \
            .get_as_input_stream(url_metadata.path)
        mimetype: str = Metadata.detect_media_type(url_metadata.path)

        if not input_stream:
            raise StorageUrlException("input stream obtained is none")

        return UrlStreaming(
            mimetype if mimetype else "application/octet-stream",
            input_stream
        )

    @abstractmethod
    def _process_url_metadata(self, url_metadata: UrlMetadata) -> str:
        """
        Provides the logic process to convert `url_metadata` to a string
        representation, which means that this representation is sufficient
        to obtain the same url_metadata with the opposite process.

        Args:
            url_metadata (UrlMetadata): The url metadata

        Returns:
            str: The url metadata processed
        """

    @abstractmethod
    def _process_metadata(self, metadata: str) -> UrlMetadata:
        """
        Provides the logic process to convert `metadata` to a UrlMetadata
        representation.

        Args:
            metadata (str): The metadata

        Returns:
            UrlMetadata: The metadata processed
        """
