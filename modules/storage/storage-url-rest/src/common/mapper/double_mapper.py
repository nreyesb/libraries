# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: double_mapper.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, final, overload
from src.common.mapper import SingleMapper

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=Any)


class DoubleMapper(SingleMapper[T, M], ABC):
    """
    The DoubleMapper Abstract Base Class.

    Provides the contract to unmap T to M and M to T.
    """

    @overload
    def unmap(self, source: M) -> T:
        """
        Unmap.

        Convert type M to T.

        Args:
            source (M): The source data to unmap.

        Returns:
            T: The unmapped result.
        """

    @overload
    def unmap(self, source: list[M]) -> list[T]:
        """
        Unmap Collection.

        Unmap the source of type M to type T and return a list.

        Args:
            source (list[M]): The source collection to unmap.

        Returns:
            list[T]: The list of unmapped results.
        """

    @final
    def unmap(self, source: M | list[M]) -> T | list[T]:
        """
        Unmap Collection.

        Unmap the source of type M to type T.

        Args:
            source (M | list[M]): The source to unmap.

        Returns:
            T | list[T]: The unmapped results.
        """
        if isinstance(source, list):
            return list(map(self.unmap, source))

        return self._unmap(source)

    @abstractmethod
    def _unmap(self, source: M) -> T:
        """
        Unmap.

        Convert type M to T.

        Args:
            source (M): The source data to unmap.

        Returns:
            T: The unmapped result.
        """
