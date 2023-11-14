# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the models for the application layer.

Classes:
    - UrlModel (url_model.py): The url model
    - DateTimeConditionModel (url_metadata_model.py): The datetime condition model of the metadata
    - ConditionModel (url_metadata_model.py): The condition model of the metadata
    - PrincipalModel (url_metadata_model.py): The principal model of the metadata
    - UrlMetadataModel (url_metadata_model.py): The url metadata model itself
"""
from .url_model import UrlModel as UrlModel
from .url_metadata_model import DateTimeConditionModel as DateTimeConditionModel
from .url_metadata_model import ConditionModel as ConditionModel
from .url_metadata_model import PrincipalModel as PrincipalModel
from .url_metadata_model import UrlMetadataModel as UrlMetadataModel
