# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: datetime_condition_verification.py
Author: Toku
"""
from overrides import override
from toku.storage.url.api.verifier import ForbiddenStorageUrlVerificationException
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime
from toku.storage.url.core import UrlMetadata
from toku.storage.url.verifier.api import Verification


class DateTimeConditionVerification(Verification):
    """
    Performs a verification to see if the datetime condition in the
    `url_metadata` are valids.
    """

    @override
    def verify(self, url_metadata: UrlMetadata) -> None:
        """
        Checks the following conditions:

        1. If `access_from` is reported and lesser or equals than now then
           accept the condition, otherwise
        2. If `access_until` is reported and greater or equals than now then
           accept the condition

        Args:
            url_metadata (UrlMetadata): The url metadata

        Raises:
            StorageUrlVerificationException: Problem with validation integrity
        """
        datetime_condition: DateTimeCondition = url_metadata.condition.datetime
        now: DateTime = DateTime.create()

        if datetime_condition.access_from and \
           now.to_millis() < DateTime.parse(datetime_condition.access_from).to_millis():
            raise ForbiddenStorageUrlVerificationException(
                f"resource will be accessible from {datetime_condition.access_from}"
            )

        if datetime_condition.access_until and \
           now.to_millis() > DateTime.parse(datetime_condition.access_until).to_millis():
            raise ForbiddenStorageUrlVerificationException(
                f"resource was accessible until {datetime_condition.access_until}"
            )
