# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: hasher.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Optional, final, overload
from overrides import EnforceOverrides


class Hasher(ABC, EnforceOverrides):
    """
    The Hasher Abstract Base Class.

    This abstract base class for hasher process provides a contract for
    hash algorithms.

    For this kind of algorithm, the real data is present in the hashertext but
    in a non-human-readable form and is undecryptable.
    """

    @overload
    def hash(self, plaintext: bytes) -> bytes:
        """
        Hashes the given `plaintext` in 'bytes'.

        If 'plaintext' is empty, it returns an empty string.

        Args:
            plaintext (str): The plaintext to hash.

        Returns:
            str: The hashertext.

        Raises:
            HasherException: If an hashing error occurs.
        """

    @overload
    def hash(self, plaintext: str, encoding: str) -> str:
        """
        Hashes the given `plaintext` in 'string' with the provided
        `encoding`

        Args:
            plaintext (str): The plaintext to hash.
            encoding (str): The encoding to use.

        Returns:
            str: The hashertext.

        Raises:
            HasherException: If an hashing error occurs.
        """

    @final
    def hash(self, plaintext: str | bytes, encoding: Optional[str] = None) -> str | bytes:
        """
        Hashes the given `plaintext`.

        Args:
            plaintext (str | bytes): The plaintext to .
            encoding (Optional[str], optional): The encoding. Defaults to None

        Returns:
            str | bytes: The hashertext.
        """
        if isinstance(plaintext, str):
            if not plaintext:
                return ""

            plaintext_as_bytes: bytes = plaintext.encode(encoding if encoding else "")
            hashertext: bytes = self.hash(plaintext_as_bytes)
            return hashertext.hex()

        return self._hash_bytes(plaintext)

    @abstractmethod
    def _hash_bytes(self, plaintext: bytes) -> bytes:
        """
        Hashes the given `plaintext` in 'bytes'.

        Args:
            plaintext (bytes): The plaintext to hash.

        Returns:
            bytes: The hashertext.

        Raises:
            HasherException: If an hashing error occurs.
        """
