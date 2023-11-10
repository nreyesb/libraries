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

Module: verification_tests.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Generator, Generic, Type, TypeVar, final
from overrides import EnforceOverrides
import pytest
from toku.storage.url.verifier import Verification
from toku.storage.url.verifier import StorageUrlVerificationException
from toku.storage.url.core import UrlMetadata


T = TypeVar("T", bound=Verification)
E = TypeVar("E", bound=StorageUrlVerificationException)

class Case(ABC, Generic[T]):
    """
    Helper class to define a dynamic test case.
    """

    def _setup(self) -> None:
        """
        Process to setup the case.
        """

    @abstractmethod
    def _create_verification(self) -> T:
        """
        Creates the verification to use in the test.

        Returns:
            UrlMetadata: The verification to test the case
        """

    @abstractmethod
    def _create_url_metadata(self) -> UrlMetadata:
        """
        Creates the url metadata to use in the test.

        Returns:
            UrlMetadata: The url metadata to test the case
        """

    @abstractmethod
    def _main_asserts(self) -> None:
        """
        Performs the main asserts.
        """

    def _additional_asserts(self) -> None:
        """
        Performs the additional asserts.
        """

    @final
    def run(self) -> None:
        """
        Run the case with the following steps:

        1. Call _setup()
        2. Call _create_verification()
        2. Call _create_url_metadata()
        3. Call _main_asserts()
        4. Call _additional_asserts()
        """
        self._setup()
        self._verification: T = self._create_verification()
        self._url_metadata: UrlMetadata = self._create_url_metadata()
        self._main_asserts()
        self._additional_asserts()


class ValidCase(Case, ABC):
    """
    Provides a valid case to test.
    """

    @final
    def _main_asserts(self) -> None:
        """
        Performs the asserts.
        """
        self._verification.verify(self._url_metadata)


class InvalidCase(Case, ABC, Generic[E]):
    """
    Provides a invalid case to test.
    """

    @abstractmethod
    def _create_exception_message(self) -> str:
        """
        Creates the exception message to assert.

        Returns:
            str: The message to assert
        """

    @abstractmethod
    def _create_exception_type(self) -> Type[E]:
        """
        Creates the exception type to assert.

        Returns:
            Type[E]: The exception type to assert
        """

    @final
    def _main_asserts(self) -> None:
        """
        Performs the asserts.
        """
        with pytest.raises(self._create_exception_type()) as exc_info:
            self._verification.verify(self._url_metadata)
        assert str(exc_info.value) == self._create_exception_message()


class VerificationTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides test cases for any kind Verification class.
    """

    def _initialize_test(self) -> None:
        """
        Common initialize processes.
        """

    def _teardown_test(self) -> None:
        """
        Common teardown processes.
        """

    @abstractmethod
    def _create_valids_cases(self) -> list[ValidCase]:
        """
        Provides a list of valids cases.

        Returns:
            list[ValidCase]: The list of valids cases.
        """

    @abstractmethod
    def _create_invalids_cases(self) -> list[InvalidCase]:
        """
        Provides a list of invalids cases.

        Returns:
            list[InvalidCase]: The list of invalids cases.
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
        self._initialize_test()

        # return control to the tests
        yield

        # teardown
        self._teardown_test()

    @pytest.fixture
    def valids_cases(self) -> list[ValidCase]:
        """
        Fixture to return a list with valids cases for verification testing.
        """
        values: list[ValidCase] = self._create_valids_cases()
        assert values
        return values

    @pytest.fixture
    def invalids_cases(self) -> list[InvalidCase]:
        """
        Fixture to return a list with invalids cases for verification testing.
        """
        values: list[InvalidCase] = self._create_invalids_cases()
        assert values
        return values

    @final
    def test_verify__valid_metadata__then_return_void(
        self,
        valids_cases: list[ValidCase]
    ) -> None:
        for case in valids_cases:
            case.run()

    @final
    def test_verify__invalid_metadata__then_raise_exception(
        self,
        invalids_cases: list[InvalidCase]
    ) -> None:
        for case in invalids_cases:
            case.run()
