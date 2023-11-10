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

Module: hasher_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Generator, final, TypeVar, Generic
from overrides import EnforceOverrides
import pytest
from toku.crypto.hasher.api import Hasher

T = TypeVar("T", bound=Hasher)


class HasherTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides test cases for any kind Hasher class.
    """

    @abstractmethod
    def _create_hasher(self) -> T:
        """
        Provides the haser instance

        Returns:
            T: The hasher instance for testing.
        """

    @abstractmethod
    def _create_hasher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        """
        Provides a list of tuples with hasher and plain texts for testing.

        The first position is the hashertext and the second the plaintext.

        Returns:
            list[tuple[str, str]]: The list of tuples with the hasher and plain texts for testing.
        """

    @abstractmethod
    def _create_hasher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        """
        Provides a list of tuples with hasher and plain texts for testing.

        The first position is the hashertext, the second the plaintext and the third the encoding.

        Returns:
            list[tuple[str, str, str]]: The list of tuples with the hasher and plain texts for testing.
        """

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        """
        Create an instance of the Hasher class for testing.

        Return the control to the test.

        Yields:
            Generator[None, None, None]: _description_
        """
        # setup
        self._hasher: T = self._create_hasher()

        # return control to the test
        yield

    @pytest.fixture
    def hasher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        """
        Fixture to return a list of tuples with hasher and plain texts for decryption testing.
        """
        values: list[tuple[bytes, bytes]] = self._create_hasher_vs_plain_texts_for_bytes()
        assert values
        return values

    @pytest.fixture
    def hasher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        """
        Fixture to return a list of tuples with hasher and plain texts for decryption testing.
        """
        values: list[tuple[str, str, str]] = self._create_hasher_vs_plain_texts_for_string()
        assert values
        return values

    @final
    def test_hash__string_value_with_empty_text__then_return_empty_string(self) -> None:
        """
        Verifies hash case for empty text.

        Args:
            hasher (T): An instance of the Hasher class for testing.
        """
        assert self._hasher.hash("", "UTF-8") == ""

    @final
    def test_hash__string_value_with_blank_text__then_return_no_empty_string(self) -> None:
        """
        Verifies hash case for blank text.

        Args:
            hasher (T): An instance of the Hasher class for testing.
        """
        assert self._hasher.hash(" ", "UTF-8") != ""

    @final
    def test_hash__string_value_with_reported_text__then_return_encrypted_string(
        self,
        hasher_vs_plain_texts_for_string: list[tuple[str, str, str]]
    ) -> None:
        """
        Every plaintext in the list `hasher_vs_plain_texts_for_string` is hashes where
        the result has to be distinct to the original plaintext and equals to
        the hashertext.

        Args:
            hasher (T): An instance of the Hasher class for testing.
            hasher_vs_plain_texts_for_string (list[tuple[str, str, str]]): Hasher and plain texts for testing
        """
        for hashertext, plaintext, encoding  in hasher_vs_plain_texts_for_string:
            hash_value: str = self._hasher.hash(plaintext, encoding)
            assert hash_value
            assert hash_value != plaintext
            assert hash_value == hashertext

    @final
    def test_hash__bytes_value_with_reported_text__then_return_encrypted_string(
        self,
        hasher_vs_plain_texts_for_bytes: list[tuple[bytes, bytes]]
    ) -> None:
        """
        Every plaintext in the list `hasher_vs_plain_texts_for_bytes` is hashes where
        the result has to be distinct to the original plaintext and equals to
        the hashertext.

        Args:
            hasher (T): An instance of the Hasher class for testing.
            hasher_vs_plain_texts_for_bytes (list[tuple[bytes, bytes]]): Hasher and plain texts for testing
        """
        for hashertext, plaintext in hasher_vs_plain_texts_for_bytes:
            hash_value: bytes = self._hasher.hash(plaintext)
            assert hash_value
            assert hash_value != plaintext
            assert hash_value == hashertext
