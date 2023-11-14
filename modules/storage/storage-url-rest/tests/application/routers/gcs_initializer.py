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

Module: gcs_initializer.py
Author: Toku
"""
from io import BufferedReader, BytesIO
import os
from typing import Optional
import uuid
from google.oauth2 import service_account  # type:ignore[import-untyped]
from google.cloud import storage  # type:ignore[import-untyped]


class GcsInitializer:
    """
    Provides the google cloud storage initializer.

    The idea is to create a root path in a bucket to work inside and delete
    the content at the end of the process.
    """

    def __init__(
        self,
        project_id: str,
        bucket_name: str,
        working_directory: Optional[str] = None,
        credentials: Optional[str] = None
    ) -> None:
        self._working_directory: str = working_directory if working_directory else self._create_directory_path()
        self._working_directory = f"{self._working_directory}/" if not self._working_directory.endswith("/") else self._working_directory

        # gcs
        sa = service_account.Credentials.from_service_account_file(
            credentials
            if credentials
            else os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        )
        self._storage = storage.Client(
            project=project_id,
            credentials=sa
        )
        self._bucket = self._storage.bucket(bucket_name)

    def start(self) -> None:
        self._make_directory(self._working_directory)

    def stop(self) -> None:
        self.clean_root()
        self._storage.close()

    def clean_root(self) -> None:
        blobs = self._bucket.list_blobs(prefix=self._working_directory)

        for blob in blobs:
            blob.delete()

    def create_directory(self, name: str | None = None) -> bool:
        return self._make_directory(
            f"{self._working_directory}{f'{name}/' if name else self._create_directory_path()}"
        )

    def create_file(self, source: bytes, file: str) -> bool:
        blob = self._bucket.blob(f"{self._working_directory}{file}")
        blob.upload_from_file(BufferedReader(BytesIO(source)))  # type: ignore[arg-type]
        return True

    def _create_directory_path(self) -> str:
        return f"{str(uuid.uuid4())}/"

    def _make_directory(self, directory: str) -> bool:
        if self._bucket:
            blob = self._bucket.blob(directory)
            blob.upload_from_string(b"")
            return True
        return False
