# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=empty-docstring
# pylint: disable=line-too-long
# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-lines
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: storage_url_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from overrides import EnforceOverrides
from toku.storage.url.api import StorageUrl

T = TypeVar("T", bound=StorageUrl)


class StorageUrlTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides the contract with the test cases for any kind StorageUrl class.
    """

    @abstractmethod
    def _initialize_test(self) -> None:
        """
        """

    @abstractmethod
    def _teardown_test(self) -> None:
        """
        """

    @abstractmethod
    def test_encode__url_empty_authority__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_encode__url_empty_path__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_encode__url_metadata_to_string_is_empty__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_encode__url_metadata_reported_full_values__then_return_url_encoded(self) -> None:
        """
        """


    @abstractmethod
    def test_decode__metadata_is_empty__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_decode__metadata_reported_full_values__then_return_url_metadata(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__url_metadata_file_doesnt_exists__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__url_metadata_datetime_acces_from_in_the_future__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__url_metadata_datetime_acces_until_in_the_past__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__input_stream_is_none__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__default_mimetype_using_file_without_extension__then_return_url_streaming(self) -> None:
        """
        """

    @abstractmethod
    def test_streaming__default_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        """
        """


    @abstractmethod
    def test_streaming__determined_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        """
        """
