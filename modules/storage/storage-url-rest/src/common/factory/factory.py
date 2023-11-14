# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: factory.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from overrides import EnforceOverrides

T = TypeVar("T", bound=Any)


class Factory(ABC, Generic[T], EnforceOverrides):
    """
    The Factory Abstract Base Class.

    Provides the contract to factory the creation of objects.
    """

    @abstractmethod
    def create(self, reference: str) -> T:
        """
        Creates an object of type T.

        Args:
            reference (str): The reference of the object to create

        Returns:
            T: The object.
        """
