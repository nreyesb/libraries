# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: cipher.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import final
from overrides import EnforceOverrides


class Cipher(ABC, EnforceOverrides):
    """
    The Cipher Abstract Base Class.

    This abstract base class for cipher process provides a contract for
    encryption and decryption for both symmetric and asymmetric algorithms.

    For this kind of algorithm, the real data is present in the ciphertext but
    in a non-human-readable form.
    """

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts the given `plaintext` in 'bytes'.

        Args:
            plaintext (bytes): The plaintext to encrypt.

        Returns:
            bytes: The ciphertext.

        Raises:
            CipherException: If an encryption error occurs.
        """

    @final
    def encrypt_string(self, plaintext: str, encoding: str) -> str:
        """
        Encrypts the given `plaintext` in 'string' with the provided
        `encoding` with the following steps:

        - If `plaintext` is empty, it returns an empty string.
        - Convert the string in bytes using `str.encode(encoding)`
        - Encrypts the bytes
        - Convert the bytes in string with `bytes.hex()`

        The final string is always in hex format.

        Args:
            plaintext (str): The plaintext to encrypt.
            encoding (str): The encoding to use.

        Returns:
            str: The ciphertext.

        Raises:
            CipherException: If an encryption error occurs.
        """
        if not plaintext:
            return ""

        plaintext_as_bytes: bytes = plaintext.encode(encoding)
        ciphertext: bytes = self.encrypt(plaintext_as_bytes)
        return ciphertext.hex()

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts the given `ciphertext` in bytes.

        Args:
            ciphertext (bytes): The ciphertext to decrypt.

        Returns:
            bytes: The plaintext.

        Raises:
            CipherException: If a decryption error occurs.
        """

    @final
    def decrypt_string(self, ciphertext: str, encoding: str) -> str:
        """
        Decrypts the given `ciphertext` in 'string' with the provided
        `encoding` with the following steps:

        - If `ciphertext` is empty, it returns an empty string.
        - Convert the string in bytes using `bytes.fromhex(ciphertext)`
        - Dencrypts the bytes
        - Convert the bytes in string with `str.decode(encoding)`

        The reported string has to be always in hex format.

        Args:
            ciphertext (str): The ciphertext to decrypt.
            encoding (str): The encoding to use.

        Returns:
            str: The plaintext.

        Raises:
            CipherException: If an encryption error occurs.
        """
        if not ciphertext:
            return ""

        ciphertext_as_bytes: bytes = bytes.fromhex(ciphertext)
        plaintext: bytes = self.decrypt(ciphertext_as_bytes)
        return plaintext.decode(encoding)
