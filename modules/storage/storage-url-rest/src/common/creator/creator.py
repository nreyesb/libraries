# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: creator.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from overrides import EnforceOverrides

T = TypeVar("T", bound=Any)


class Creator(ABC, Generic[T], EnforceOverrides):
    """
    The Creator Abstract Base Class.

    Provides the contract to create an object.
    """

    @abstractmethod
    def create(self) -> T:
        """
        Creates an object of type T.

        Returns:
            T: The object.
        """
