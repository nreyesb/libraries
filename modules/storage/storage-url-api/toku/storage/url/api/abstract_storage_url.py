# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: abstract_storage_url.py
Author: Toku
"""
from abc import ABC, abstractmethod
from io import BufferedReader
import os
from typing import Optional, final
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.api import Metadata
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded
from toku.storage.url.core import UrlStreaming
from toku.storage.url.core import StorageUrlException
from toku.storage.url.verifier.api import Verification
from toku.storage.url.api import StorageUrl
from toku.storage.url.api.verifier import FileExistsVerification
from toku.storage.url.api.verifier import DateTimeConditionVerification


class AbstractStorageUrl(StorageUrl, ABC):
    """
    The `AbstractStorageUrl` class provides a base for working with storage url.
    """

    @final
    @override
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> UrlEncoded:
        # process url_metadata to get a string and check if it's not empty
        # create the url encoded with the url and the metadata as string
        metadata: str = self._process_url_metadata(url_metadata)

        if not metadata.strip():
            raise StorageUrlException("url_metadata processed is empty")

        return UrlEncoded(
            url.schema,
            url.authority,
            url.path,
            metadata
        )

    @final
    @override
    def decode(self, metadata: str) -> UrlMetadata:
        if not metadata.strip():
            raise StorageUrlException("metadata to decode is empty")

        return self._process_metadata(metadata)

    @final
    @override
    def streaming(
        self,
        storage_driver: StorageDriver,
        url_metadata: UrlMetadata,
        verifications: Optional[list[Verification]] = None
    ) -> UrlStreaming:
        # apply verifications
        #   determines if the file exists
        #   apply custom verifications
        #   apply datetome condition verifications
        # get the inputstream
        # get the mimetype or 'application/octet-strea' by default
        # create the url encoded and return
        FileExistsVerification(storage_driver).verify(url_metadata)

        if verifications:
            for verification in verifications:
                verification.verify(url_metadata)

        DateTimeConditionVerification().verify(url_metadata)

        input_stream: Optional[BufferedReader] = storage_driver \
            .get_as_input_stream(url_metadata.path)
        mimetype: str = Metadata.detect_media_type(url_metadata.path)

        if not input_stream:
            raise StorageUrlException("input stream obtained is none")

        return UrlStreaming(
            name=os.path.basename(url_metadata.path),
            content_type=mimetype if mimetype else "application/octet-stream",
            data=input_stream
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
