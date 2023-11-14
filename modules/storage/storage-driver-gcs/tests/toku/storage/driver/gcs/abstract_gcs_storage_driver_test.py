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

Module: abstract_gcs_storage_driver_tests.py
Author: Toku
"""
from abc import ABC
import os
from typing import Any, Generator
import uuid
from google.oauth2 import service_account  # type:ignore[import-untyped]
from google.cloud import storage  # type:ignore[import-untyped]
from overrides import override
import pytest
from tests.toku.storage.driver.api import AbstractStorageDriverTest
from toku.storage.driver.gcs import GcsStorageDriver


class AbstractGcsStorageDriverTest(AbstractStorageDriverTest[GcsStorageDriver], ABC):
    """
    Provides the google cloud storage driver tests.

    To run the tests is required to set the following environment variables:

    - GCP_PROJECT_ID = It's the id of the GCP project
    - GCP_BUCKET_NAME = It's the name of the bucket
    - GCP_CREDENTIALS_FILE = It's the JSON credentials file (a service account is recommended)

    To do that it's possible to run `export {variable}={value}`

    The tests will not create the bucket, but it considerers to delete the created
    root folder for the tests to clean the bucket.
    """

    GCP_PROJECT_ID: str = ""
    GCP_BUCKET_NAME: str = ""
    GCP_CREDENTIALS: str = ""
    BUCKET: Any | None = None
    WD: str = ""

    @override
    def _initialize_test(self) -> None:
        self._working_directory_primary_storage_driver: str = self._create_directory_path_in_root()
        self._working_directory_secondary_storage_driver: str = self._create_directory_path_in_root()

        self._make_directory(self._working_directory_primary_storage_driver)
        self._make_directory(self._working_directory_secondary_storage_driver)

    @override
    def _teardown_test(self) -> None:
        pass  # not needed

    def _create_directory_path(self) -> str:
        return f"{str(uuid.uuid4())}/"

    def _create_directory_path_in_root(self, name: str | None = None) -> str:
        return f"{AbstractGcsStorageDriverTest.WD}{f'{name}/' if name else self._create_directory_path()}"

    def _make_directory(self, directory: str) -> bool:
        if AbstractGcsStorageDriverTest.BUCKET:
            blob = AbstractGcsStorageDriverTest.BUCKET.blob(directory)
            blob.upload_from_string(b"")
            return True
        return False

    @pytest.fixture(scope="class", autouse=True)
    def setup_tests(self) -> Generator[None, None, None]:
        # setup
        AbstractGcsStorageDriverTest.GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "")
        AbstractGcsStorageDriverTest.GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME", "")
        AbstractGcsStorageDriverTest.GCP_CREDENTIALS = os.environ.get("GCP_CREDENTIALS_FILE", "")
        AbstractGcsStorageDriverTest.WD = self._create_directory_path()

        credentials = service_account.Credentials.from_service_account_file(AbstractGcsStorageDriverTest.GCP_CREDENTIALS)
        self._storage = storage.Client(
            project=AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            credentials=credentials
        )
        AbstractGcsStorageDriverTest.BUCKET = self._storage.bucket(AbstractGcsStorageDriverTest.GCP_BUCKET_NAME)
        self._make_directory(AbstractGcsStorageDriverTest.WD)

        # return control to the test
        yield

        # teardown
        blobs = AbstractGcsStorageDriverTest.BUCKET.list_blobs(prefix=AbstractGcsStorageDriverTest.WD)

        for blob in blobs:
            blob.delete()

        self._storage.close()

    @override
    def test_open__successful_driver_initialization__then_return_void(self) -> None:
        storage_driver: GcsStorageDriver = self._create_storage_driver()
        storage_driver.open()

    @override
    def test_open__unsuccessful_driver_initialization__then_raise_exception(self) -> None:
        storage_driver = GcsStorageDriver(
            self._working_directory_secondary_storage_driver,
            f"invalid-project-{str(uuid.uuid4())}",
            AbstractGcsStorageDriverTest.GCP_BUCKET_NAME,
            AbstractGcsStorageDriverTest.GCP_CREDENTIALS
        )
        with pytest.raises(Exception):
            storage_driver.open()

        storage_driver = GcsStorageDriver(
            self._working_directory_secondary_storage_driver,
            AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            f"invalid-bucket-{str(uuid.uuid4())}",
            AbstractGcsStorageDriverTest.GCP_CREDENTIALS
        )
        with pytest.raises(Exception):
            storage_driver.open()

        storage_driver = GcsStorageDriver(
            self._working_directory_secondary_storage_driver,
            AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            AbstractGcsStorageDriverTest.GCP_BUCKET_NAME,
            f"invalid-credentials{str(uuid.uuid4())}"
        )
        with pytest.raises(Exception):
            storage_driver.open()

    @override
    def test_close__successful_driver_completion__then_return_void(self) -> None:
        storage_driver = GcsStorageDriver(
            self._working_directory_primary_storage_driver,
            AbstractGcsStorageDriverTest.GCP_PROJECT_ID,
            AbstractGcsStorageDriverTest.GCP_BUCKET_NAME,
            AbstractGcsStorageDriverTest.GCP_CREDENTIALS
        )
        storage_driver.open()
        storage_driver.close()
