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
from typing import Optional, Type


class HasherException(Exception):
    """
    Represents a Hasher exception.
    """

    def __init__(self, message: Optional[str] = None, cause: Type[Exception] | None = None) -> None:
        """Initialize the StorageDriverException.

        Args:
            message (Optional[str]): A description of the error. Defaults to None.
            cause (Exception): The exception that caused this error. Defaults to None.
        """
        super().__init__(message)
        self.cause: type[Exception] | None = cause
