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
from flexmock import flexmock
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.api.verifier import FileExistsVerification
from tests.toku.storage.driver.api import StubStorageDriver
from tests.toku.storage.url.verifier import VerificationTest
from tests.toku.storage.url.verifier import ValidCase
from tests.toku.storage.url.verifier import InvalidCase


class MetatadaPathExistsInStorageDriverValidCase(ValidCase):

    def _setup(self) -> None:
        self._path: str = "directory/file.txt"
        self._storage_driver = StubStorageDriver()
        flexmock(self._storage_driver).should_receive("exists").with_args(self._path).and_return(True).once()

    def _create_verification(self) -> FileExistsVerification:
        return FileExistsVerification(self._storage_driver)

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            path=self._path,
            storage_driver_reference=""
        ) \
        .build()


class MetatadaPathDoesntExistsInStorageDriverValidCase(InvalidCase):

    def _setup(self) -> None:
        self._path: str = "directory/file.txt"
        self._storage_driver = StubStorageDriver()
        flexmock(self._storage_driver).should_receive("exists").with_args(self._path).and_return(False).once()

    def _create_verification(self) -> FileExistsVerification:
        return FileExistsVerification(self._storage_driver)

    def _create_url_metadata(self) -> UrlMetadata:
        return UrlMetadata.builder(
            path=self._path,
            storage_driver_reference=""
        ) \
        .build()

    def _create_exception_message(self) -> str:
        return f"file {self._path} doesn't exists"


class DateTimeConditionVerificationTests(VerificationTest[FileExistsVerification]):
    """
    Provides test cases for DateTimeConditionVerification class.
    """

    @override
    def _create_valids_cases(self) -> list[ValidCase]:
        return [
            MetatadaPathExistsInStorageDriverValidCase()
        ]

    @override
    def _create_invalids_cases(self) -> list[InvalidCase]:
        return [
            MetatadaPathDoesntExistsInStorageDriverValidCase()
        ]
