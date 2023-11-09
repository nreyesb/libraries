# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the StorageUrl API.

Classes:
    - StorageUrl (storage_url.py): The contract for storage url process
    - AbstractStorageUrl (abstract_storage_url.py): The default implementation for storage url process
    - StorageUrlDecorator (storage_url_decorator.py): The base for any storage url decorator
"""
from .storage_url import StorageUrl as StorageUrl
from .abstract_storage_url import AbstractStorageUrl as AbstractStorageUrl
from .storage_url_decorator import StorageUrlDecorator as StorageUrlDecorator
