# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the inbounds aka UseCases of the domain layer, to declare
how the application layer can interact with the domain layer.

Classes:
    - UrlDecodeUseCase (url_decode_use_case.py): The use case to decode an url
    - UrlEncodeUseCase (url_encode_use_case.py): The use case to encode an url
    - UrlStreamingUseCase (url_streaming_use_case.py): The use case to streaming an url
"""
from .url_decode_use_case import UrlDecodeUseCase as UrlDecodeUseCase
from .url_encode_use_case import UrlEncodeUseCase as UrlEncodeUseCase
from .url_streaming_use_case import UrlStreamingUseCase as UrlStreamingUseCase
