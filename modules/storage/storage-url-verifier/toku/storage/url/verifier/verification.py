# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: verification.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from toku.storage.url.core import UrlMetadata


class Verification(ABC):
    """
    Perform a verification on the `metadata` of `UrlMetadata` type.
    """

    @abstractmethod
    def verify(self, url_metadata: UrlMetadata) -> None:
        """
        Perform a validation on the `metadata`.

        Args:
            url_metadata (UrlMetadata): The url metadata to be validated.
        """
