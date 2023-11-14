# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_streaming_repository.py
Author: Toku
"""
from dataclasses import dataclass
from typing import Any, Literal, Self
from overrides import override
from toku.storage.driver.api import StorageDriver
from toku.storage.url.api import StorageUrl
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlStreaming
from src.common.factory import Factory
from src.domain.port.outbounds import UrlStreamingPort


@dataclass
class UrlStreamingWrapper(UrlStreaming):
    """
    Provides the url streaming wrapper, to close the input stream and the driver
    after it was readed.
    """

    def __init__(
        self,
        url_streaming: UrlStreaming,
        storage_driver: StorageDriver
    ) -> None:
        super().__init__(
            name=url_streaming.name,
            content_type=url_streaming.content_type,
            data=url_streaming.data
        )
        self._storage_driver: StorageDriver = storage_driver

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type_: Any, exc_value_: Any, traceback_: Any) -> Literal[False]:
        try:
            super().__exit__(exc_type_, exc_value_, traceback_)
        finally:
            self._storage_driver.close()
        return False  # indicates that exceptions should be propagated


class UrlStreamingRepository(UrlStreamingPort):
    """
    Provides the repository to streaming an URL.
    """

    def __init__(
            self,
            storage_driver_factory: Factory[StorageDriver],
            storage_url: StorageUrl
    ) -> None:
        """
        Initialize the UrlStreamingRepository.

        The process uses the `UrlStreamingWrapper` to return a `UrlStreaming`
        but additionaly closing the internal `storage_driver` created.

        Args:
            storage_driver_factory (Factory): The storage driver factory
            storage_url (StorageUrl): The storage url to streaming the URL
        """
        self._storage_driver_factory: Factory = storage_driver_factory
        self._storage_url: StorageUrl = storage_url

    @override
    def streaming(self, url_metadata: UrlMetadata) -> UrlStreaming:
        storage_drive: StorageDriver = self._storage_driver_factory.create(
            url_metadata.storage_driver_reference
        )
        storage_drive.open()
        url_streaming: UrlStreaming = self._storage_url.streaming(
            storage_drive,
            url_metadata,
            verifications=[]
        )

        return UrlStreamingWrapper(
            url_streaming,
            storage_drive
        )
