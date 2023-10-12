# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: sha_hasher.py
Author: Toku Dev
"""
from enum import Enum
import hashlib
from typing import final
from overrides import override
from toku.hasher.api import Hasher


class Type(str, Enum):
    """
    Indicates the AES type supported.
    """

    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"


class ShaHasher(Hasher):
    """
    Provides an SHA implementation for hash.
    """

    def __init__(self, sha_type: Type) -> None:
        """
        Initializes the ShaHasher instance with the provided type.

        Args:
            sha_type (Type):
                The SHA type to use.

                - sha1
                - sha256
                - sha512
        """
        self.sha_type: Type = sha_type

    @final
    @override
    def hash(self, plaintext: str | None) -> str:
        if not plaintext:
            return ""

        hasher = hashlib.new(self.sha_type)
        hasher.update(plaintext.encode("utf-8"))
        return hasher.hexdigest()
