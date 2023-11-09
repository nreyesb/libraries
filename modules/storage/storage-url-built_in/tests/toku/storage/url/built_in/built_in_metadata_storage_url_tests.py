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

Module: built_in_metadata_storage_url_tests.py
Author: Toku
"""
from typing import final
from overrides import override
from toku.storage.url.built_in import BuiltInMetadataStorageUrl
from tests.toku.storage.url.api import AbstractStorageUrlTest


@final
class BuiltInMetadataStorageUrlTests(AbstractStorageUrlTest[BuiltInMetadataStorageUrl]):
    """
    Provides the built-in metadata storage url tests.
    """

    @override
    def _initialize_test(self) -> None:
        pass  # not needed

    @override
    def _teardown_test(self) -> None:
        pass  # not needed

    @override
    def _create_storage_url(self) -> BuiltInMetadataStorageUrl:
        return BuiltInMetadataStorageUrl(b'8d7asbjkdbask8o7')
