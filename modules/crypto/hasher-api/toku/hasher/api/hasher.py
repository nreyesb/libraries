# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: hasher.py
Author: Toku Dev
"""
from abc import ABC, abstractmethod
from overrides import EnforceOverrides


class Hasher(ABC, EnforceOverrides):
    """
    The Hasher Abstract Base Class.

    This abstract base class for hasher process provides a contract for
    hash algorithms.
    """

    @abstractmethod
    def hash(self, plaintext: str | None) -> str:
        """
        Hashes the given plaintext.

        If 'plaintext' is None or empty, it returns an empty string.

        Args:
            plaintext (str): The plaintext to hash.

        Returns:
            str: The hashertext.

        Raises:
            HasherException: If an encryption error occurs.
        """
