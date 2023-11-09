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

Module: url_tests.py
Author: Toku
"""
import pytest
from toku.storage.url.core import Url
from toku.storage.url.core import UrlSchema
from toku.storage.url.core import StorageUrlException


class UrlTests:
    """
    Provides test cases for class Url class.
    """

    def test_to_url__empty_authority__then_raise_exception(self) -> None:
        url_encoded = Url(
            UrlSchema.HTTP,
            "",
            "path"
        )
        with pytest.raises(StorageUrlException) as exc_info:
            url_encoded.to_url()

        assert str(exc_info.value) == "authority can't be empty"

    def test_to_url__empty_path__then_raise_exception(self) -> None:
        url_encoded = Url(
            UrlSchema.HTTP,
            "authority",
            ""
        )
        with pytest.raises(StorageUrlException) as exc_info:
            url_encoded.to_url()

        assert str(exc_info.value) == "path can't be empty"

    def test_to_url__reported_values__then_return_string(self) -> None:
        url_encoded = Url(
            UrlSchema.HTTP,
            "www.my-domain.com",
            "storage/url/streaming"
        )
        assert url_encoded.to_url() == "http://www.my-domain.com/storage/url/streaming"
