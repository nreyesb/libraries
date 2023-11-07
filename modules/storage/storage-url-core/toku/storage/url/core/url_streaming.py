# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_streaming.py
Author: Toku Dev
"""
from dataclasses import dataclass
from io import BufferedReader
from typing import Any, Literal, Self


@dataclass
class UrlStreaming:
    """
    Provides the streaming with the `content_type` and the `data` to get a resource.
    """

    content_type: str  # the mimetype of the `data` to use in TCP/IP
    data: BufferedReader  # the data as input stream

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type_: Any, exc_value_: Any, traceback_: Any) -> Literal[False]:
        self.data.close()
        return False  # indicates that exceptions should be propagated
