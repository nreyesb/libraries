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
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import Principal
from toku.storage.url.api.verifier import PrincipalVerification
from tests.toku.storage.url.verifier import VerificationTest
from tests.toku.storage.url.verifier import ValidCase
from tests.toku.storage.url.verifier import InvalidCase


class VerificationPrincipalIsEmptyAndMetatadaPrincipalIsEmptyValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal(""))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal("")) \
        .build()


class VerificationPrincipalIsEmptyAndMetatadaPrincipalIsEveryoneValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal(""))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal.everyone()) \
        .build()


class VerificationPrincipalIsEmptyAndMetatadaPrincipalIsDefaultValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal(""))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .build()


class VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsTheSameValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal("USER_NAME"))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal("USER_NAME")) \
        .build()


class VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsEveryoneValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal("USER_NAME"))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal.everyone()) \
        .build()


class VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsDefaultValidCase(ValidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal("USER_NAME"))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .build()


class VerificationPrincipalIsEmptyAndMetatadaPrincipalIsNotEmptyInvalidCase(InvalidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal(""))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal("USER_NAME")) \
        .build()

    def _create_exception_message(self) -> str:
        return "authorized principal is 'USER_NAME' not ''"


class VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsEmptyInvalidCase(InvalidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal("USER_NAME"))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal("")) \
        .build()

    def _create_exception_message(self) -> str:
        return "authorized principal is '' not 'USER_NAME'"


class VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsNotEmptyButDifferentsInvalidCase(InvalidCase):

    def _create_verification(self) -> PrincipalVerification:
        return PrincipalVerification(Principal("USER_NAME"))

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            "",
            ""
        ) \
        .principal(Principal("USER_NAMe")) \
        .build()

    def _create_exception_message(self) -> str:
        return "authorized principal is 'USER_NAMe' not 'USER_NAME'"


class PrincipalVerificationTests(VerificationTest[PrincipalVerification]):
    """
    Provides test cases for PrincipalVerification class.
    """

    @override
    def _create_valids_cases(self) -> list[ValidCase]:
        return [
            VerificationPrincipalIsEmptyAndMetatadaPrincipalIsEmptyValidCase(),
            VerificationPrincipalIsEmptyAndMetatadaPrincipalIsEveryoneValidCase(),
            VerificationPrincipalIsEmptyAndMetatadaPrincipalIsDefaultValidCase(),
            VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsTheSameValidCase(),
            VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsEveryoneValidCase(),
            VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsDefaultValidCase()
        ]

    @override
    def _create_invalids_cases(self) -> list[InvalidCase]:
        return [
            VerificationPrincipalIsEmptyAndMetatadaPrincipalIsNotEmptyInvalidCase(),
            VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsEmptyInvalidCase(),
            VerificationPrincipalIsNotEmptyAndMetatadaPrincipalIsNotEmptyButDifferentsInvalidCase()
        ]
