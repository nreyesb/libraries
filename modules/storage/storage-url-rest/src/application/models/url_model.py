# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_model.py
Author: Toku
"""
from pydantic import BaseModel, Field
from toku.storage.url.core import UrlSchema


class UrlModel(BaseModel):
    """
    Provide the application model for Url.
    """

    url_schema: UrlSchema = Field(
        ...,
        description="The schema type to get the resource"
    )
    authority: str = Field(
        ...,
        description="The domain to get the resource, for example: www.my-domain.com"
    )
    path: str = Field(
        ...,
        description="The endpoint path to get the resource, for example: streaming/get/{metadata}"
    )
