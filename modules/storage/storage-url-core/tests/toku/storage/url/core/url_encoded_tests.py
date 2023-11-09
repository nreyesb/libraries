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

Module: url_encoded_tests.py
Author: Toku
"""
import pytest
from toku.storage.url.core import UrlEncoded
from toku.storage.url.core import UrlSchema


class UrlEncodedTests:
    """
    Provides test cases for class UrlEncoded class.
    """

    def test_to_url__empty_authority__then_raise_exception(self) -> None:
        url_encoded = UrlEncoded(
            UrlSchema.HTTP,
            "",
            "path",
            "metadata"
        )
        with pytest.raises(Exception) as exc_info:
            url_encoded.to_url()

        assert str(exc_info.value) == "authority can't be empty"

    def test_to_url__empty_path__then_raise_exception(self) -> None:
        url_encoded = UrlEncoded(
            UrlSchema.HTTP,
            "authority",
            "",
            "metadata"
        )
        with pytest.raises(Exception) as exc_info:
            url_encoded.to_url()

        assert str(exc_info.value) == "path can't be empty"

    def test_to_url__empty_metadata__then_raise_exception(self) -> None:
        url_encoded = UrlEncoded(
            UrlSchema.HTTP,
            "authority",
            "path",
            ""
        )
        with pytest.raises(Exception) as exc_info:
            url_encoded.to_url()

        assert str(exc_info.value) == "metadata can't be empty"

    def test_to_url__path_without_metadata_to_replace__then_return_string_without_metadata(self) -> None:
        url_encoded = UrlEncoded(
            UrlSchema.HTTP,
            "www.my-domain.com",
            "storage/url/streaming",
            "a9s087dygsabkhjy0d8as798f7ti6asthgfcv"
        )
        assert url_encoded.to_url() == "http://www.my-domain.com/storage/url/streaming"

    def test_to_url__all_correct_values__then_return_string(self) -> None:
        url_encoded = UrlEncoded(
            UrlSchema.HTTP,
            "www.my-domain.com",
            "storage/url/streaming/{metadata}",
            "a9s087dygsabkhjy0d8as798f7ti6asthgfcv"
        )
        assert url_encoded.to_url() == "http://www.my-domain.com/storage/url/streaming/a9s087dygsabkhjy0d8as798f7ti6asthgfcv"
