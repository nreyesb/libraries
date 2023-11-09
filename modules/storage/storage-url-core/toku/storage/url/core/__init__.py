# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the StorageUrl Core.

Classes:
    - StorageUrlException (storage_url_exception.py): The storage url exception
    - UrlSchema (url_schema.py): The possible url schemas
    - UrlStreaming (url_streaming.py): The url streaming to get a resource
    - Url (url.py): The url
    - UrlEncoded (url_encoded.py): The url encoded to get a resource
    - DateTime (url_metadata.py): The datetime wrapper
    - Classification (url_metadata.py): The classification of the metadata
    - DateTimeCondition (url_metadata.py): The datetime condition of the metadata
    - Condition (url_metadata.py): The condition of the metadata
    - Principal (url_metadata.py): The principal of the metadata
    - UrlMetadata (url_metadata.py): The url metadata itself
    - UrlMetadataBuilder (url_metadata.py): The builder of the url metadata
"""
from .storage_url_exception import StorageUrlException as StorageUrlException
from .url_schema import UrlSchema as UrlSchema
from .url_streaming import UrlStreaming as UrlStreaming
from .url import Url as Url
from .url_encoded import UrlEncoded as UrlEncoded
from .url_metadata import DateTime as DateTime
from .url_metadata import Classification as Classification
from .url_metadata import DateTimeCondition as DateTimeCondition
from .url_metadata import Condition as Condition
from .url_metadata import Principal as Principal
from .url_metadata import UrlMetadata as UrlMetadata
from .url_metadata import UrlMetadataBuilder as UrlMetadataBuilder
