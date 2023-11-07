# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=missing-function-docstring
# pylint: disable=empty-docstring
# pylint: disable=line-too-long
# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-lines
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_metadata_tests.py
Author: Toku Dev
"""
from datetime import datetime, timedelta
import re
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import Classification
from toku.storage.url.core import Principal
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime


class UrlMetadataTests:
    """
    Provides test cases for class UrlMetadata class.
    """

    def test_builder__minimum_data__then_return_url_metadata(self) -> None:
        url_metadata: UrlMetadata = UrlMetadata \
            .builder(
                path="minimum-data/file.txt",
                storage_driver_reference="storage_reference_min"
            ) \
            .build()

        assert url_metadata
        assert re.match(r'^[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+$', url_metadata.id)
        assert url_metadata.created_at <= int(datetime.utcnow().timestamp() * 1000)
        assert url_metadata.path == "minimum-data/file.txt"
        assert url_metadata.storage_driver_reference == "storage_reference_min"
        assert url_metadata.classification == Classification.PUBLIC
        assert url_metadata.principal == Principal.everyone()
        assert url_metadata.condition.datetime.access_from == 0
        assert url_metadata.condition.datetime.access_until == 0
        assert not url_metadata.metadata

    def test_builder__full_data__then_return_url_metadata(self) -> None:
        access_from: DateTime = DateTime.create()
        access_until: DateTime = DateTime.create(access_from.get()).delta(timedelta(hours=2, days=4))

        url_metadata: UrlMetadata = UrlMetadata \
            .builder(
                path="full-data/file.txt",
                storage_driver_reference="storage_reference_max"
            ) \
            .classification(Classification.CONFIDENTIAL) \
            .principal(Principal("USER")) \
            .condition(Condition(
                DateTimeCondition(
                    access_from=access_from.to_millis(),
                    access_until=access_until.to_millis()
                )
            )) \
            .metadata({
                "key1": "value1",
                "key2": "value2"
            }) \
            .build()

        assert url_metadata
        assert re.match(r'^[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+$', url_metadata.id)
        assert url_metadata.created_at <= int(datetime.utcnow().timestamp() * 1000)
        assert url_metadata.path == "full-data/file.txt"
        assert url_metadata.storage_driver_reference == "storage_reference_max"
        assert url_metadata.classification == Classification.CONFIDENTIAL
        assert url_metadata.principal == Principal("USER")
        assert DateTime.from_millis(url_metadata.condition.datetime.access_from).to_millis() == access_from.to_millis()
        assert DateTime.from_millis(url_metadata.condition.datetime.access_until).to_millis() == access_until.to_millis()
        assert url_metadata.metadata == {"key1": "value1","key2": "value2"}
