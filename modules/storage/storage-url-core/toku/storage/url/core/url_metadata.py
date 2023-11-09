# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_metadata.py
Author: Toku
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import os
from typing import Dict, Self
import uuid


class DateTime:
    """
    Provides a wrapper for datetime to work in UTC timezone.
    """

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f %Z"

    def __init__(self, date_time: datetime) -> None:
        """
        Create a new datetime.

        By default, the process always uses UTC timezone.

        Args:
            date_time (datetime): The datetime.
        """
        self._datetime: datetime = date_time.replace(tzinfo=timezone.utc)

    @staticmethod
    def create(date_time: datetime = datetime.now(timezone.utc)) -> 'DateTime':
        """
        Create a new DateTime.

        See __init__(...)

        Args:
            date_time (datetime, optional): The datetime. Defaults to datetime.now(timezone.utc)).

        Returns:date
            DateTime: The new DateTime.
        """
        return DateTime(date_time)

    @staticmethod
    def parse(date_time: str) -> 'DateTime':
        """
        Parse the `date_time` with the following format '%Y-%m-%d %H:%M:%S.%f %Z',

        For example: 2023-11-07 11:45.42 UTC

        See __init__(...)

        Returns:
            DateTime: The new DateTime.
        """
        datetime_utc: datetime = datetime.strptime(date_time, DateTime.DATETIME_FORMAT)
        return DateTime(datetime_utc)

    def delta(self, delta: timedelta) -> Self:
        """
        Apply a `delta` to the internal datetime.

        Args:
            delta (timedelta): The delta.

        Returns:
            Self: Itself.
        """
        self._datetime = self._datetime + delta
        return self

    def to_millis(self) -> int:
        """
        Return the datetime as millis.

        Returns:
            int: datetime as millis.
        """
        return int(self._datetime.timestamp() * 1000)

    def to_string(self) -> str:
        """
        Return the datetime as string.

        Returns:
            str: datetime as string.
        """
        return self._datetime.strftime(DateTime.DATETIME_FORMAT)


class Classification(Enum):
    """
    Provides the differents levels of data classification.

    - PUBLIC       = Doesn't contain sensitive information, which doesn't expose
                     anything relevant about entities related to the company

    - PRIVATE      = Doesn't contain sensitive information, nevertheles it
                     should not be exposed as public

    - INTERNAL     = Contains sensitive information, which doesn't exposes critical
                     data about entities related to the company

    - CONFIDENTIAL = Contains sensitive information, exposing critical data
                     about entities related to the company but should not have
                     legal problems

    - RESTRICTED   = Contains sensitive information, exposing critical data
                     about entities related to the company implying possible
                     legal problems
    """

    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


@dataclass
class DateTimeCondition:
    """
    Provides the conditions for the lifespan of data access
    """

    access_from: str = ""  # UTC time. Default None infinite.
    access_until: str = ""  # UTC time. Default None infinite.


@dataclass
class Condition:
    """
    Provides the conditions of data access
    """

    datetime: DateTimeCondition = field(default_factory=DateTimeCondition)  # the datetime condition


@dataclass
class Principal:
    """
    Indicates who was give access to the data
    """

    name: str  # it's the name of the principal

    @staticmethod
    def everyone() -> 'Principal':
        """
        Provides the default principal.

        Returns:
            Principal: The "EVERYONE" principal
        """
        return Principal("EVERYONE")


@dataclass
class UrlMetadata:
    """
    Provides the metadata of a resource.

    Recommended to use the builder static method to instanciate the Builder
    class to create an instance of `UrlMetadata`.
    """

    id: str  # the unique identifier of the url metadata
    created_at: int  # indicates in UTC when was created the metadata
    path: str  # the full path of the resource inside the storage driver
    storage_driver_reference: str  # the reference to create the storage driver
    classification: Classification  # the classification of the data
    principal: Principal  # who can access to the data
    condition: Condition  # the condition to get the data
    metadata: Dict[str, str]  # additional metadata that could be used by verifiers

    @staticmethod
    def builder(
        path: str,
        storage_driver_reference: str
    ) -> 'UrlMetadataBuilder':
        """
        Create a Builder for UrlMetadata.

        Args:
            path (str): The full path of the resource inside the storage driver.
            storage_driver_reference (str): The reference to create the storage driver.

        Returns:
            UrlMetadataBuilder: The builder.
        """
        return UrlMetadataBuilder(
            path,
            storage_driver_reference
        )


class UrlMetadataBuilder:
    """
    Builder class for UrlMetadata.
    """

    def __init__(
            self,
            path: str,
            storage_driver_reference: str
    ) -> None:
        """
        Create a new Builder for UrlMetadata.

        It requires only mandatory attributes, the others have a default value:

        classification = Classification.PUBLIC
        principal = Principal.everyone()
        condition = Condition()
        metadata = {}

        id is always a UUID with uuid.NAMESPACE_DNS and an urandom of size 128.
        created_at is always the time in millis of the current date in UTC.

        Args:
            path (str): The full path of the resource inside the storage driver.
            storage_driver_reference (str): The reference to create the storage driver.
        """
        self._id: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(os.urandom(128))))
        self._created_at: int = DateTime.create().to_millis()
        self._path: str = path
        self._storage_driver_reference: str = storage_driver_reference
        self._classification: Classification = Classification.PUBLIC
        self._principal: Principal = Principal.everyone()
        self._condition: Condition = Condition()
        self._metadata: Dict[str, str] = {}

    def classification(self, classification: Classification) -> 'UrlMetadataBuilder':
        """
        Sets the classification.

        Args:
            classification (Classification): The classification of the data.

        Returns:
            UrlMetadataBuilder: Itself.
        """
        self._classification = classification
        return self

    def principal(self, principal: Principal) -> 'UrlMetadataBuilder':
        """_summary_

        Args:
            principal (Principal): Who can access to the data.

        Returns:
            UrlMetadataBuilder: Itself.
        """
        self._principal = principal
        return self

    def condition(self, condition: Condition) -> 'UrlMetadataBuilder':
        """
        Sets the condition.

        Args:
            condition (Condition): The condition to get the data.

        Returns:
            UrlMetadataBuilder: Itself.
        """
        self._condition = condition
        return self

    def metadata(self, metadata: Dict[str, str]) -> 'UrlMetadataBuilder':
        """
        Sets the metadata.

        Args:
            metadata (Dict[str, str]): Additional metadata that could be used by verifiers.

        Returns:
            UrlMetadataBuilder: Itself.
        """
        self._metadata = metadata
        return self

    def build(self) -> UrlMetadata:
        """
        Builds the UrlMetada.

        Returns:
            UrlMetadata: The url metadata.
        """
        return UrlMetadata(
            self._id,
            self._created_at,
            self._path,
            self._storage_driver_reference,
            self._classification,
            self._principal,
            self._condition,
            self._metadata
        )
