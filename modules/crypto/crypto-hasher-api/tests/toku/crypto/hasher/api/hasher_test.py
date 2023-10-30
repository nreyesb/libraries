# -*- coding: utf-8 -*-
# flake8: noqa: E501
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: hasher_test.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from typing import final, TypeVar, Generic
from overrides import EnforceOverrides
import pytest
from toku.crypto.hasher.api import Hasher

T = TypeVar("T", bound=Hasher)


class HasherTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides test cases for any kind Hasher class.
    """

    @pytest.fixture
    def hasher(self) -> T:
        """
        Fixture to return an instance of the Hasher class for testing.
        """
        hasher: T = self._create_hasher()
        assert hasher
        return hasher

    @pytest.fixture
    def plain_vs_hasher_texts(self) -> dict[str, str]:
        """
        Fixture to return a dict with plain vs hasher texts for testing.
        """
        values: dict[str, str] = self._create_plain_vs_hasher_texts()
        assert values
        return values

    @final
    def test_hash__with_none_text__then_return_empty_string(self, hasher: T) -> None:
        """
        Verifies hash case for none text.

        Args:
            hasher (T): An instance of the Hasher class for testing.
        """
        assert hasher.hash(None) == ""

    @final
    def test_hash__with_empty_text__then_return_empty_string(self, hasher: T) -> None:
        """
        Verifies hash case for empty text.

        Args:
            hasher (T): An instance of the Hasher class for testing.
        """
        assert hasher.hash("") == ""

    @final
    def test_hash__with_blank_text__then_return_no_empty_string(self, hasher: T) -> None:
        """
        Verifies hash case for blank text.

        Args:
            hasher (T): An instance of the Hasher class for testing.
        """
        assert hasher.hash(" ") != ""

    @final
    def test_hash__with_reported_text__then_return_encrypted_string(
        self, hasher: T, plain_vs_hasher_texts: dict[str, str]
    ) -> None:
        """
        Verifies hashes case for not none and not empty text.

        Every plaintext in the dict plain_vs_hasher_texts is hashes where
        the result has to be distinct to the original plaintext and equals to
        the hashertext.

        Args:
            hasher (T): An instance of the Hasher class for testing.
            plain_vs_hasher_texts (dict[str, str]): Plain vs hasher texts for testing
        """
        for plaintext, hashertext in plain_vs_hasher_texts.items():
            hash_value: str = hasher.hash(plaintext)
            assert hash_value
            assert hash_value != plaintext
            assert hash_value == hashertext

    @abstractmethod
    def _create_hasher(self) -> T:
        """
        Provides the haser instance

        Returns:
            T: The hasher instance for testing.
        """

    @abstractmethod
    def _create_plain_vs_hasher_texts(self) -> dict[str, str]:
        """
        Provides a dict with plain vs hasher texts for testing.

        Returns:
            dict[str, str]: The dict with the plain and hasher texts for testing.
        """
