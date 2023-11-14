# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_url.py
Author: Toku
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides
from toku.storage.driver.api import StorageDriver
from toku.storage.url.core import Url
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded
from toku.storage.url.core import UrlStreaming
from toku.storage.url.verifier.api import Verification


class StorageUrl(ABC, EnforceOverrides):
    """
    Provides the contract to define the abstraction to use the storage url to
    get a resource from an URL.
    """

    @abstractmethod
    def encode(
        self,
        url: Url,
        url_metadata: UrlMetadata
    ) -> UrlEncoded:
        """
        Provides the process to create the `UrlEncoded` based on the `UrlMetadata`
        and the `Url` to create the URL itself to get the resource.

        View the `UrlEncoded` for more details, because it corresponds to a
        representation of an URL with the `UrlMetadata` itself but using it as
        string representation, finally the exposed URL uses a special string to
        replace the string metadata in the url.

        The final URL has to be an url safe.

        View the `decode` method to do the opposite process.

        Args:
            schema (UrlSchema): The schema type to get the resource.
            authority (str): The domain to get the resource,
                             for example: www.my-domain.com.
            path (str): The endpoint path to get the resource,
                        for example: streaming/get/{metadata}.
            url_metadata (UrlMetada): The url metadata

        Returns:
            UrlEncode: The url encoded
        """

    @abstractmethod
    def decode(self, metadata: str) -> UrlMetadata:
        """
        Provides the process to create the `UrlMetadata` based on the `metadata`
        which was created in the `encode` method.

        View the `encode` method to do the opposite process.

        Args:
            metadata (str): The metadata as string

        Returns:
            UrlMetadata: The url metadata
        """

    @abstractmethod
    def streaming(
        self,
        storage_driver: StorageDriver,
        url_metadata: UrlMetadata,
        verifications: list[Verification]
    ) -> UrlStreaming:
        """
        Provides the process to get the resource of the `url_metadata` as an
        input stream applying all the `verifications` needed to know if it's
        possible to get the resource.

        Args:
            url_metadata (UrlMetadata): The url metadata
            verifications (st[Verification]): The verifications to apply in the url_metadata

        Returns:
            UrlStreaming: The url streaming
        """
