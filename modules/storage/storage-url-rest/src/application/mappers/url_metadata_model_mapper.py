# -*- coding: utf-8 -*-
"""
Private License - For Tnternal Use Mnly

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_metadata_model_mapper.py
Author: Toku
"""
from dataclasses import asdict
from overrides import override
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import Principal
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import UrlMetadataBuilder
from src.application.models import UrlMetadataModel
from src.application.models import PrincipalModel
from src.application.models import ConditionModel
from src.application.models import DateTimeConditionModel
from src.common.mapper import DoubleMapper


class PrincipalModelMapper(DoubleMapper[PrincipalModel, Principal]):
    """
    The PrincipalModelMapper implementation.

    Provides the mapper from `PrincipalModel` to `Principal` and vice versa.
    """

    @override
    def _map(self, source: PrincipalModel) -> Principal:
        return Principal(*source.model_dump().values())

    @override
    def _unmap(self, source: Principal) -> PrincipalModel:
        return PrincipalModel(**asdict(source))


class DateTimeConditionModelMapper(DoubleMapper[DateTimeConditionModel, DateTimeCondition]):
    """
    The DateTimeConditionModelMapper implementation.

    Provides the mapper from `DateTimeConditionModel` to `DateTimeCondition` and vice versa.
    """

    @override
    def _map(self, source: DateTimeConditionModel) -> DateTimeCondition:
        return DateTimeCondition(*source.model_dump().values())

    @override
    def _unmap(self, source: DateTimeCondition) -> DateTimeConditionModel:
        return DateTimeConditionModel(**asdict(source))


class ConditionModelMapper(DoubleMapper[ConditionModel, Condition]):
    """
    The ConditionModelMapper implementation.

    Provides the mapper from `ConditionModel` to `Condition` and vice versa.
    """

    @override
    def _map(self, source: ConditionModel) -> Condition:
        data = {}

        if source.datetime:
            data["datetime"] = DateTimeCondition(*source.datetime.model_dump().values())

        return Condition(**data)

    @override
    def _unmap(self, source: Condition) -> ConditionModel:
        return ConditionModel(
            datetime=DateTimeConditionModelMapper().unmap(source.datetime)
        )


class UrlMetadataModelMapper(DoubleMapper[UrlMetadataModel, UrlMetadata]):
    """
    The UrlMetadataModelMapper implementation.

    Provides the mapper from `UrlMetadataModel` to `UrlMetadata` and the vice versa.
    """

    @override
    def _map(self, source: UrlMetadataModel) -> UrlMetadata:
        url_metadata_builder: UrlMetadataBuilder = UrlMetadata.builder(
            path=source.path,
            storage_driver_reference=source.storage_driver_reference
        )

        if source.classification:
            url_metadata_builder.classification(source.classification)

        if source.principal:
            url_metadata_builder.principal(PrincipalModelMapper().map(source.principal))

        if source.condition:
            url_metadata_builder.condition(ConditionModelMapper().map(source.condition))

        if source.metadata:
            url_metadata_builder.metadata(source.metadata)

        return url_metadata_builder.build()

    @override
    def _unmap(self, source: UrlMetadata) -> UrlMetadataModel:
        return UrlMetadataModel(
            path=source.path,
            id=source.id,
            created_at=source.created_at,
            storage_driver_reference=source.storage_driver_reference,
            classification=source.classification,
            principal=PrincipalModelMapper().unmap(source.principal),
            condition=ConditionModelMapper().unmap(source.condition),
            metadata=source.metadata
        )
