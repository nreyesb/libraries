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

Module: cipher_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Generator, final, TypeVar, Generic
from overrides import EnforceOverrides
import pytest
from toku.crypto.cipher.api import Cipher

T = TypeVar("T", bound=Cipher)


class CipherTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides test cases for any kind Cipher class.
    """

    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        """
        Create an instance of the Cipher class for testing.

        Return the control to the test.

        Yields:
            Generator[None, None, None]: _description_
        """
        # setup
        self._cipher: T = self._create_cipher()

        # return control to the tests
        yield

    @pytest.fixture
    def plain_texts(self) -> list[str]:
        """
        Fixture to return a list with plain texts for encryption testing.
        """
        values: list[str] = self._create_plain_texts()
        assert values
        return values

    @pytest.fixture
    def cipher_vs_plain_texts(self) -> dict[str, str]:
        """
        Fixture to return a dict with cipher and plain texts for decryption testing.
        """
        values: dict[str, str] = self._create_cipher_vs_plain_texts()
        assert values
        return values

    @final
    def test_encrypt__with_none_text__then_return_empty_string(self) -> None:
        """
        Verifies encryption case for none text.

        Args:
            cipher (T): An instance of the Cipher class for testing.
        """
        assert self._cipher.encrypt(None) == ""

    @final
    def test_encrypt__with_empty_text__then_return_empty_string(self) -> None:
        """
        Verifies encryption case for empty text.

        Args:
            cipher (T): An instance of the Cipher class for testing.
        """
        assert self._cipher.encrypt("") == ""

    @final
    def test_encrypt__with_blank_text__then_return_no_empty_string(self) -> None:
        """
        Verifies encryption case for blank text.

        Args:
            cipher (T): An instance of the Cipher class for testing.
        """
        assert self._cipher.encrypt(" ") != ""

    @final
    def test_encrypt__with_reported_text__then_return_encrypted_string(
        self,
        plain_texts: list[str]
    ) -> None:
        """
        Verifies encryption case for not none and not empty text.

        Every plaintext in the list plain_texts is encrypted and then decrypted
        the result has to be the same plaintext.

        Args:
            cipher (T): An instance of the Cipher class for testing.
            plain_texts (list[str]): Plain texts for testing
        """
        for plaintext in plain_texts:
            ciphertext: str = self._cipher.encrypt(plaintext)
            assert ciphertext
            assert ciphertext != plaintext
            assert self._cipher.decrypt(ciphertext) == plaintext

    @final
    def test_decrypt__with_none_text__then_return_empty_string(self) -> None:
        """
        Verifies decryption case for none text.

        Args:
            cipher (T): An instance of the Cipher class for testing.
        """
        assert self._cipher.decrypt(None) == ""

    @final
    def test_decrypt__with_empty_text__then_return_empty_string(self) -> None:
        """
        Verifies decryption case for empty text.

        Args:
            cipher (T): An instance of the Cipher class for testing.
        """
        assert self._cipher.decrypt("") == ""

    @final
    def test_decrypt__with_reported_text__then_return_decrypted_string(
        self,
        cipher_vs_plain_texts: dict[str, str]
    ) -> None:
        """
        Verifies decryption case for not none and not empty text.

        Every ciphertext in the dict is decrypted and compared with the plaintext.

        Args:
            cipher (T): An instance of the Cipher class for testing.
            cipher_vs_plain_texts (dict[str, str]): Cipher and plain texts for testing
        """
        for ciphertext, plaintext in cipher_vs_plain_texts.items():
            assert self._cipher.decrypt(ciphertext) == plaintext

    @abstractmethod
    def _create_cipher(self) -> T:
        """
        Provides the cipher instance

        Returns:
            T: The cipher instance for testing.
        """

    @abstractmethod
    def _create_plain_texts(self) -> list[str]:
        """
        Provides a list with plain texts for testing.

        Returns:
            list[str]: The list with the plaintexts for testing.
        """

    @abstractmethod
    def _create_cipher_vs_plain_texts(self) -> dict[str, str]:
        """
        Provides a dict with cipher and plain texts for testing.

        The first position is the ciphertext and the second the plaintext.

        Returns:
            dict[str, str]: The dict with the cipher and plain texts for testing.
        """
