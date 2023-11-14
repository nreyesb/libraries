# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the factories of the infrastructure layer.

Classes:
    - StorageDriverFactory (storage_driver_factory.py): The storage driver factory
    - StorageUrlFactory (storage_url_factory.py): The storage url factory
"""
from .storage_driver_factory import StorageDriverFactory as StorageDriverFactory
from .storage_url_factory import StorageUrlFactory as StorageUrlFactory
