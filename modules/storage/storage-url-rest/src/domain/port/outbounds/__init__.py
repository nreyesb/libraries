# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the outbounds ports of the domain layer, to declare how
the domain layer can interact with the infrastructure layer.

Classes:
    - UrlDecodePort (url_decode_port.py): The port to decode an url
    - UrlEncodePort (url_encode_port.py): The port to encode an url
    - UrlStreamingPort (url_streaming_port.py): The port to streaming an url
"""
from .url_decode_port import UrlDecodePort as UrlDecodePort
from .url_encode_port import UrlEncodePort as UrlEncodePort
from .url_streaming_port import UrlStreamingPort as UrlStreamingPort
