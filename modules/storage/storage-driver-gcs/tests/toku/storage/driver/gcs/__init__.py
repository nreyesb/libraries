# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the StorageDriver API for testing purpose.

Classes:
    - AbstractGcsStorageDriverTest (abstract_gcs_storage_driver_test.py): Provides the abstract GCS storage driver tests
    - ReportedCredentialsGcsStorageDriverTests (reported_crendentials_gcs_storage_driver_tests.py): Provides the reported service account GCS storage driver tests
    - EnvironmentCredentialsGcsStorageDriverTests (environment_crendentials_gcs_storage_driver_tests.py): Provides the environment service account GCS storage driver tests
"""
from .abstract_gcs_storage_driver_test import AbstractGcsStorageDriverTest as AbstractGcsStorageDriverTest
from .reported_crendentials_gcs_storage_driver_tests import ReportedCredentialsGcsStorageDriverTests as ReportedCredentialsGcsStorageDriverTests
from .environment_crendentials_gcs_storage_driver_tests import EnvironmentCredentialsGcsStorageDriverTests as EnvironmentCredentialsGcsStorageDriverTests
