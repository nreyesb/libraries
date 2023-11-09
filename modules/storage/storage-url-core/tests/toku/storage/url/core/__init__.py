# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the StorageUrl Core for testing purpose.

Classes:
    - UrlTests (url_tests.py): Url tests
    - UrlEncodedTests (url_encoded_tests.py): Url encoded tests
    - UrlMetadataTests (url_metadata_tests.py): Url metadata tests
    - UrlStreamingTests (url_streaming_tests.py): Url streaming tests
"""
from .url_tests import UrlTests as UrlTests
from .url_encoded_tests import UrlEncodedTests as UrlEncodedTests
from .url_metadata_tests import UrlMetadataTests as UrlMetadataTests
from .url_streaming_tests import UrlStreamingTests as UrlStreamingTests
