# -*- coding: utf-8 -*-
# flake8: noqa: E501
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

Module: verification_tests.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from typing import Generator, Generic, TypeVar
from overrides import EnforceOverrides
import pytest
from toku.storage.url.verifier import Verification
from toku.storage.url.core import UrlMetadata


T = TypeVar("T", bound=Verification)


class VerificationTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides test cases for any kind Verification class.
    """

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        """
        Create an instance of the Verification class for testing.

        Start the setup process (sub-class).

        Return the control to the test.

        Start the teardown process (sub-class).

        Yields:
            Generator[None, None, None]: _description_
        """
        # setup
        self._verification: T = self._create_verification()
        self._initialize_test()

        # return control to the tests
        yield

        # teardown
        self._teardown_test()

    @pytest.fixture
    def valids_metadata(self) -> list[UrlMetadata]:
        """
        Fixture to return a list with valids metadata for verification testing.
        """
        values: list[UrlMetadata] = self._create_valids_metadata()
        assert values
        return values

    @pytest.fixture
    def invalids_metadata(self) -> dict[UrlMetadata, str]:
        """
        Fixture to return a dict with invalids metadata for verification testing.
        """
        values: dict[UrlMetadata, str] = self._create_invalids_metadata()
        assert values
        return values

    @abstractmethod
    def test_verify__valid_metadata__then_return_void(
        self,
        valids_metadata: list[UrlMetadata]
    ) -> None:
        for url_metadata in valids_metadata:
            self._verification.verify(url_metadata)

    @abstractmethod
    def test_verify__invalid_metadata__then_raise_exception(
        self,
        invalids_metadata: dict[UrlMetadata, str]
    ) -> None:
        url_metadata: UrlMetadata
        message: str
        for url_metadata, message in invalids_metadata.items():
            with pytest.raises(Exception) as exc_info:
                self._verification.verify(url_metadata)
            assert str(exc_info.value) == message

    @abstractmethod
    def _initialize_test(self) -> None:
        """
        """

    @abstractmethod
    def _teardown_test(self) -> None:
        """
        """

    @abstractmethod
    def _create_verification(self) -> T:
        """
        Provides the verification instance.

        Returns:
            T: The verification instance for testing.
        """

    @abstractmethod
    def _create_valids_metadata(self) -> list[UrlMetadata]:
        """
        Provides a list of valids metadata.

        Returns:
            list[UrlMetadata]: The list with valids metadata.
        """

    @abstractmethod
    def _create_invalids_metadata(self) -> dict[UrlMetadata, str]:
        """
        Provides a dict of invalids metadata.
        The second position is the message of the exception.

        Returns:
            dict[UrlMetadata, str]: The dict with invalids metadata.
        """
