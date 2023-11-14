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

Module: reported_crendentials_gcs_storage_driver_tests.py
Author: Toku
"""
from typing import final
from overrides import override
from tests.toku.storage.driver.gcs import AbstractGcsStorageDriverTest
from toku.storage.driver.gcs import GcsStorageDriver


@final
class ReportedCredentialsGcsStorageDriverTests(AbstractGcsStorageDriverTest):
    """
    Provides the google cloud storage driver tests for a service account
    reported in the constructor.

    See parent class.
    """

    @override
    def _create_storage_driver(self) -> GcsStorageDriver:
        return GcsStorageDriver(
            self._working_directory_primary_storage_driver,
            AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            AbstractGcsStorageDriverTest.GCP_BUCKET_NAME,
            AbstractGcsStorageDriverTest.GCP_CREDENTIALS
        )

    @override
    def _create_storage_driver_secondary(self) -> GcsStorageDriver:
        return GcsStorageDriver(
            self._working_directory_secondary_storage_driver,
            AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            AbstractGcsStorageDriverTest.GCP_BUCKET_NAME,
            AbstractGcsStorageDriverTest.GCP_CREDENTIALS
        )
