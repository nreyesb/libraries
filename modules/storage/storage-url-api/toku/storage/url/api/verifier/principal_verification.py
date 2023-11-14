# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: principal_verification.py
Author: Toku
"""
from overrides import override
from toku.storage.url.api.verifier import UnauthorizedStorageUrlVerificationException
from toku.storage.url.core import Principal
from toku.storage.url.core import UrlMetadata
from toku.storage.url.verifier.api import Verification


class PrincipalVerification(Verification):
    """
    Performs a verification to see if the principal reported matches with the
    `url_metadata`.
    """

    def __init__(self, principal: Principal) -> None:
        """
        Create a new principal verification.

        Args:
            principal (Principal): The principal
        """
        self._principal: Principal = principal

    @override
    def verify(self, url_metadata: UrlMetadata) -> None:
        """
        Checks if the principal in the `url_metadata` matches with the
        `self._principal` following this conditions:

        1. If the principal in the `url_metadata` is everyone then accept the
           condition, otherwise
        2. If the principal in the `url_metadata` is equals to `self._principal`
           then accept the condition

        Args:
            url_metadata (UrlMetadata): The url metadata

        Raises:
            StorageUrlVerificationException: Problem with validation integrity
        """
        principal: Principal = url_metadata.principal

        if principal.name == Principal.everyone().name:
            return

        if principal.name != self._principal.name:
            raise UnauthorizedStorageUrlVerificationException(
                f"authorized principal is '{principal.name}' not '{self._principal.name}'"
            )
