# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: cipher.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides


class Cipher(ABC, EnforceOverrides):
    """
    The Cipher Abstract Base Class.

    This abstract base class for cipher process provides a contract for
    encryption and decryption for both symmetric and asymmetric algorithms.
    """

    @abstractmethod
    def encrypt(self, plaintext: str | None) -> str:
        """
        Encrypts the given plaintext.

        If 'plaintext' is None or empty, it returns an empty string.

        Args:
            plaintext (str): The plaintext to encrypt.

        Returns:
            str: The ciphertext.

        Raises:
            CipherException: If an encryption error occurs.
        """

    @abstractmethod
    def decrypt(self, ciphertext: str | None) -> str:
        """
        Decrypts the given ciphertext.

        If 'ciphertext' is None or empty, it returns an empty string.

        Args:
            ciphertext (str): The ciphertext to decrypt.

        Returns:
            str: The plaintext.

        Raises:
            CipherException: If a decryption error occurs.
        """
