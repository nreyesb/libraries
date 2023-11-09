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

Module: url_streaming_tests.py
Author: Toku
"""
from io import BufferedReader, BytesIO

import pytest
from toku.storage.url.core import UrlStreaming


class UrlStreamingTests:
    """
    Provides test cases for class UrlStreaming class.
    """

    @pytest.fixture
    def create_url_streaming(self) -> UrlStreaming:
        return UrlStreaming(
            "application/octet-stream",
            BufferedReader(BytesIO(b"text"))  # type: ignore[arg-type]
        )

    def test_data_close__no_interaction_after_closing__then_return_void(
        self,
        create_url_streaming: UrlStreaming
    ) -> None:
        with create_url_streaming as url_streaming:
            assert url_streaming.data.read() == b"text"
            url_streaming.data.seek(0)
            assert url_streaming.data.read() == b"text"
            assert url_streaming.data.read() == b""

    def test_data_close__interaction_after_closing__then_raise_exception(
        self,
        create_url_streaming: UrlStreaming
    ) -> None:
        with create_url_streaming as url_streaming:
            assert url_streaming.data.read() == b"text"
            url_streaming.data.seek(0)
            assert url_streaming.data.read() == b"text"
            assert url_streaming.data.read() == b""

        with pytest.raises(Exception) as exc_info:
            url_streaming.data.seek(0)
        assert str(exc_info.value) == "seek of closed file"
