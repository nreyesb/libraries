# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: hasher_exception.py
Author: Toku Dev
"""


class HasherException(Exception):
    """
    Represents a Hasher exception.
    """

    def __init__(self, message: str) -> None:
        """
        Instantiates a new Hasher exception.

        Args:
            message (str): The message for the exception.
        """
        super().__init__(message)
