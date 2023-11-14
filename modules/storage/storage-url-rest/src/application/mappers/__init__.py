# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the application mappers for the application layer.

Classes:
    - UrlModelMapper (url_model_mapper.py): The url model mapper to convert `UrlModel` to `Url`
    - UrlMetadataModelMapper (url_metadata_model_mapper.py): The url metadata model mapper to convert `UrlMetadataModel` to `UrlMetadata`
"""
from .url_model_mapper import UrlModelMapper as UrlModelMapper
from .url_metadata_model_mapper import UrlMetadataModelMapper as UrlMetadataModelMapper
