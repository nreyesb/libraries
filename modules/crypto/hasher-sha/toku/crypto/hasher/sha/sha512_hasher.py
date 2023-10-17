# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: sha521_hasher.py
Author: Toku Dev
"""
from toku.crypto.hasher.sha import ShaHasher
from toku.crypto.hasher.sha import ShaType


class Sha512Hasher(ShaHasher):
    """
    Provides an SHA512 implementation for hash.
    """

    def __init__(self) -> None:
        """
        Initializes the Sha512Hasher.
        """
        super().__init__(ShaType.SHA512)
