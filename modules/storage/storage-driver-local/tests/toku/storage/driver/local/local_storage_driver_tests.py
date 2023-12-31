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

Module: local_storage_driver_tests.py
Author: Toku
"""
import os
from typing import final
import uuid
from overrides import override
import pytest
from tests.toku.storage.driver.api import AbstractStorageDriverTest
from toku.storage.driver.local import LocalStorageDriver


@final
class LocalStorageDriverTests(AbstractStorageDriverTest[LocalStorageDriver]):
    """
    Provides the local storage driver tests.
    """

    @override
    def _initialize_test(self) -> None:
        self._working_directory_primary_storage_driver: str = self._create_working_directory()
        self._working_directory_secondary_storage_driver: str = self._create_working_directory()

    @override
    def _teardown_test(self) -> None:
        pass  # not needed

    @override
    def _create_storage_driver(self) -> LocalStorageDriver:
        return LocalStorageDriver(self._working_directory_primary_storage_driver)

    @override
    def _create_storage_driver_secondary(self) -> LocalStorageDriver:
        return LocalStorageDriver(self._working_directory_secondary_storage_driver)

    def _create_working_directory(self) -> str:
        temp_dir: str = os.path.join(self._tempdir.name, str(uuid.uuid4()))
        os.mkdir(temp_dir)
        return temp_dir

    @override
    def test_open__successful_driver_initialization__then_return_void(self) -> None:
        assert os.path.exists(self._tempdir.name)
        storage_driver = LocalStorageDriver(self._tempdir.name)
        storage_driver.open()

    @override
    def test_open__unsuccessful_driver_initialization__then_raise_exception(self) -> None:
        root: str = os.path.join("/c", str(uuid.uuid4()))
        storage_driver = LocalStorageDriver(root)
        assert not os.path.exists(root)
        with pytest.raises(Exception) as exc_info:
            storage_driver.open()
        assert str(exc_info.value) == f"root {root} is not a directory"

    @override
    def test_close__successful_driver_completion__then_return_void(self) -> None:
        assert os.path.exists(self._tempdir.name)
        storage_driver = LocalStorageDriver(self._tempdir.name)
        storage_driver.open()
        storage_driver.close()
