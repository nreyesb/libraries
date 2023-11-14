# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_metadata_model.py
Author: Toku
"""
from typing import Dict
from pydantic import BaseModel, Field
from toku.storage.url.core import Classification


class DateTimeConditionModel(BaseModel):
    """
    Provide the application model for DateTimeConditionModel.
    """

    access_from: str = Field(
        "",
        description="UTC time. Default None infinite."
    )
    access_until: str = Field(
        "",
        description="UTC time. Default None infinite."
    )


class ConditionModel(BaseModel):
    """
    Provide the application model for ConditionModel.
    """

    datetime: DateTimeConditionModel = Field(
        None,
        description="The datetime condition"
    )


class PrincipalModel(BaseModel):
    """
    Provide the application model for PrincipalModel.
    """

    name: str = Field(...)


class UrlMetadataModel(BaseModel):
    """
    Provide the application model for class UrlMetadataModel(BaseModel).
    """
    id: str = Field(
        None,
        description="The unique identifier of the url metadata"
    )
    created_at: str = Field(
        None,
        description="Indicates in UTC when was created the metadata"
    )
    path: str = Field(
        ...,
        description="The full path of the resource inside the storage driver"
    )
    storage_driver_reference: str = Field(
        ...,
        description="The reference to create the storage driver"
    )
    classification: Classification = Field(
        None,
        description="The classification of the data"
    )
    principal: PrincipalModel = Field(
        None,
        description="Who can access to the data"
    )
    condition: ConditionModel = Field(
        None,
        description="The condition to get the data"
    )
    metadata: Dict[str, str] = Field(
        None,
        description="Additional metadata that could be used by verifiers"
    )
