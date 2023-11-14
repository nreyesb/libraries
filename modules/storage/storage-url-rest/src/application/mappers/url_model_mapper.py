# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_model_mapper.py
Author: Toku
"""
from overrides import EnforceOverrides, override
from toku.storage.url.core import Url
from src.application.models import UrlModel
from src.common.mapper import SingleMapper


class UrlModelMapper(SingleMapper[UrlModel, Url], EnforceOverrides):
    """
    The UrlModelMapper implementation.

    Provides the mapper from `UrlModel` to `Url`.
    """

    @override
    def _map(self, source: UrlModel) -> Url:
        return Url(*source.model_dump().values())
