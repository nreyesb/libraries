# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=empty-docstring
# pylint: disable=line-too-long
# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-lines
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: aes_cipher_tests.py
Author: Toku
"""
from datetime import timedelta
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime
from toku.storage.url.api.verifier import DateTimeConditionVerification
from tests.toku.storage.url.verifier import VerificationTest
from tests.toku.storage.url.verifier import ValidCase
from tests.toku.storage.url.verifier import InvalidCase


class MetatadaDateTimeConditionIsDefaultValidCase(ValidCase):

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .build()


class MetatadaDateTimeConditionIsBetweenACorrectIntervalValidCase(ValidCase):

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .condition(Condition(
            DateTimeCondition(
                access_from=DateTime.create().to_string(),
                access_until=DateTime.create().delta(timedelta(seconds=1)).to_string()
            )
        )) \
        .build()


class MetatadaDateTimeConditionOnlyHasAccessFrom2SecondsInThePastValidCase(ValidCase):

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .condition(Condition(
            DateTimeCondition(
                access_from=DateTime.create().delta(timedelta(seconds=-2)).to_string()
            )
        )) \
        .build()


class MetatadaDateTimeConditionOnlyHasAccessUntil2SecondsInTheFutureValidCase(ValidCase):

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .condition(Condition(
            DateTimeCondition(
                access_until=DateTime.create().delta(timedelta(seconds=2)).to_string()
            )
        )) \
        .build()


class MetatadaDateTimeConditionOnlyHasAccessFrom30SecondsInTheFutureInvalidCase(InvalidCase):

    def _setup(self) -> None:
        self._access_from: str = DateTime.create().delta(timedelta(seconds=30)).to_string()

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .condition(Condition(
            DateTimeCondition(
                access_from=self._access_from
            )
        )) \
        .build()

    def _create_exception_message(self) -> str:
        return f"resource will be accessible from {self._access_from}"


class MetatadaDateTimeConditionOnlyHasAccessUntil30SecondsInThePastInvalidCase(InvalidCase):

    def _setup(self) -> None:
        self._access_until: str = DateTime.create().delta(timedelta(seconds=-30)).to_string()

    def _create_verification(self) -> DateTimeConditionVerification:
        return DateTimeConditionVerification()

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .condition(Condition(
            DateTimeCondition(
                access_until=self._access_until
            )
        )) \
        .build()

    def _create_exception_message(self) -> str:
        return f"resource was accessible until {self._access_until}"


class DateTimeConditionVerificationTests(VerificationTest[DateTimeConditionVerification]):
    """
    Provides test cases for DateTimeConditionVerification class.
    """

    @override
    def _create_valids_cases(self) -> list[ValidCase]:
        return [
            MetatadaDateTimeConditionIsDefaultValidCase(),
            MetatadaDateTimeConditionIsBetweenACorrectIntervalValidCase(),
            MetatadaDateTimeConditionOnlyHasAccessFrom2SecondsInThePastValidCase(),
            MetatadaDateTimeConditionOnlyHasAccessUntil2SecondsInTheFutureValidCase()
        ]

    @override
    def _create_invalids_cases(self) -> list[InvalidCase]:
        return [
            MetatadaDateTimeConditionOnlyHasAccessFrom30SecondsInTheFutureInvalidCase(),
            MetatadaDateTimeConditionOnlyHasAccessUntil30SecondsInThePastInvalidCase()
        ]
