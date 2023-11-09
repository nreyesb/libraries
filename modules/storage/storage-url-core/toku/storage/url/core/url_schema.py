# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_schema.py
Author: Toku
"""
from enum import Enum


class UrlSchema(Enum):
    """
    Provides the possibles url schema values for the storage url.
    """

    HTTP = "http"
    HTTPS = "https"
