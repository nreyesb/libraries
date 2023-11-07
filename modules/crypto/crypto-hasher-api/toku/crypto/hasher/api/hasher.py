# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: hasher.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from typing import Optional
from overrides import EnforceOverrides


class Hasher(ABC, EnforceOverrides):
    """
    The Hasher Abstract Base Class.

    This abstract base class for hasher process provides a contract for
    hash algorithms.

    For this kind of algorithm, the real data is present in the ciphertext but
    in a non-human-readable form and is undecryptable.
    """

    @abstractmethod
    def hash(self, plaintext: Optional[str]) -> str:
        """
        Hashes the given plaintext.

        If 'plaintext' is None or empty, it returns an empty string.

        Args:
            plaintext (Optional[str]): The plaintext to hash.

        Returns:
            str: The hashertext.

        Raises:
            HasherException: If an encryption error occurs.
        """
