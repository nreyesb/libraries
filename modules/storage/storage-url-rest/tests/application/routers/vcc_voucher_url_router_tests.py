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

Module: vcc_voucher_url_router_tests.py
Author: Toku
"""
import os
from overrides import override
from tests.application.routers import GcsInitializer
from tests.application.routers import UrlRouterTest


class VccVoucherUrlRouterTests(UrlRouterTest):
    """
    Provides the vcc voucher url endpoint test cases.
    """

    @override
    def _initialize_test(self) -> None:
        self._gcs_initializer: GcsInitializer = GcsInitializer(
            project_id=os.getenv("STORAGE_URL_GCS_VCC_VOUCHER_PROJECT_ID", ""),
            bucket_name=os.getenv("STORAGE_URL_GCS_VCC_VOUCHER_BUCKET_NAME", ""),
            working_directory=os.getenv("STORAGE_URL_VCC_GCS_VOUCHER_ROOT", "")
        )

    @override
    def _teardown_test(self) -> None:
        self._gcs_initializer.stop()

    @override
    def _initialize_streaming_test(self) -> None:
        self._gcs_initializer.start()
        self._gcs_initializer.create_directory(UrlRouterTest.STORAGE_DRIVER_DIRECTORY)
        self._gcs_initializer.create_file(
            source=bytes(self._content_with_extension, "utf-8"),
            file=UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION
        )
        self._gcs_initializer.create_file(
            source=bytes(self._content_without_extension, "utf-8"),
            file=UrlRouterTest.STORAGE_DRIVER_PATH_WITHOUT_EXTENSION
        )

    @override
    def _teardown_streaming_test(self) -> None:
        self._gcs_initializer.clean_root()

    @override
    def _get_storage_driver_reference(self) -> str:
        return "VCC-VOUCHER"
