# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: sha256_hasher.py
Author: Toku
"""
from typing import final
from toku.crypto.hasher.sha import ShaHasher
from toku.crypto.hasher.sha import ShaType


@final
class Sha256Hasher(ShaHasher):
    """
    Provides an SHA256 implementation for hash.
    """

    def __init__(self) -> None:
        """
        Initializes the Sha256Hasher.
        """
        super().__init__(ShaType.SHA256)
