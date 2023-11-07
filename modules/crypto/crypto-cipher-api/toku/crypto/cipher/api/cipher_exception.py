# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: cipher_exception.py
Author: Toku Dev
"""
from typing import Optional


class CipherException(Exception):
    """
    Represents a Cipher exception.
    """

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize the CipherException.

        Args:
            message (Optional[str]): A description of the error. Defaults to None.
        """
        super().__init__(message)
