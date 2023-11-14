# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: single_mapper.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, final, overload
from overrides import EnforceOverrides

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=Any)


class SingleMapper(ABC, Generic[T, M], EnforceOverrides):
    """
    The SingleMapper Abstract Base Class.

    Provides the contract to map T to M.
    """

    @overload
    def map(self, source: T) -> M:
        """
        Map.

        Convert type T to M.

        Args:
            source (T): The source data to map.

        Returns:
            M: The mapped result.
        """

    @overload
    def map(self, source: list[T]) -> list[M]:
        """
        Map Collection.

        Map the source of type T to type M and return a list.

        Args:
            source (list[T]): The source collection to map.

        Returns:
            list[M]: The list of mapped results.
        """

    @final
    def map(self, source: T | list[T]) -> M | list[M]:
        """
        Map Collection.

        Map the source of type T to type M.

        Args:
            source (T | list[T]): The source to map.

        Returns:
            M | list[M]: The mapped results.
        """
        if isinstance(source, list):
            return list(map(self.map, source))

        return self._map(source)

    @abstractmethod
    def _map(self, source: T) -> M:
        """
        Map.

        Convert type T to M.

        Args:
            source (T): The source data to map.

        Returns:
            M: The mapped result.
        """
