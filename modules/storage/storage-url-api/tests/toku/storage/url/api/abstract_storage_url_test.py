# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=missing-class-docstring
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

Module: abstract_storage_url_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from datetime import timedelta
from io import BufferedReader, BytesIO
import re
from typing import Generator, Generic, TypeVar, final
from faker import Faker
from flexmock import flexmock
from overrides import EnforceOverrides, override
import pytest
from tests.toku.storage.driver.api import StubStorageDriver
from tests.toku.storage.url.api import StorageUrlTest
from toku.storage.url.api import AbstractStorageUrl
from toku.storage.url.core import Url
from toku.storage.url.core import UrlSchema
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import UrlEncoded
from toku.storage.url.core import UrlStreaming
from toku.storage.url.core import Classification
from toku.storage.url.core import Principal
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime
from toku.storage.url.core import StorageUrlException

T = TypeVar("T", bound=AbstractStorageUrl)


class AbstractStorageUrlTest(StorageUrlTest[T], ABC, EnforceOverrides, Generic[T]):
    """
    Provides the default implementation for test cases for any kind AbstractStorageUrl class.
    """

    @final
    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        """
        Start the setup process (sub-class).

        Initialize the `storage_url` and the `faker`.

        Return the control to the test.

        Start the teardown process (sub-class).

        Yields:
            Generator[None, None, None]: To return the control to the test and after that finishing the test
        """
        # setup
        self._initialize_test()
        self._storage_url: T = self._create_storage_url()
        self._faker = Faker()

        # return control to the test
        yield

        # teardown
        self._teardown_test()


    @final
    @override
    def test_encode__url_empty_authority__then_raise_exception(self) -> None:
        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.encode(
                url=Url(
                    UrlSchema.HTTP,
                    "",
                    "path"
                ),
                url_metadata=UrlMetadata \
                    .builder(
                        path="",
                        storage_driver_reference=""
                    ) \
                    .build()
            )

        assert str(exc_info.value) == "authority can't be empty"

    @final
    @override
    def test_encode__url_empty_path__then_raise_exception(self) -> None:
        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.encode(
                url=Url(
                    UrlSchema.HTTP,
                    "authority",
                    ""
                ),
                url_metadata=UrlMetadata \
                    .builder(
                        path="",
                        storage_driver_reference=""
                    ) \
                    .build()
            )

        assert str(exc_info.value) == "path can't be empty"

    @final
    @override
    def test_encode__url_metadata_to_string_is_empty__then_raise_exception(self) -> None:
        path = "directory/file.txt"
        url_metadata: UrlMetadata = UrlMetadata \
            .builder(
                path=path,
                storage_driver_reference=""
            ) \
            .build()
        flexmock(self._storage_url).should_receive("_process_url_metadata").with_args(url_metadata).and_return("").once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.encode(
                url=Url(
                    UrlSchema.HTTP,
                    "www.my-domain.com",
                    "v1/streaming/{metadata}"
                ),
                url_metadata=url_metadata
            )

        assert str(exc_info.value) == "url_metadata processed is empty"

    @final
    @override
    def test_encode__url_metadata_reported_full_values__then_return_url_encoded(self) -> None:
        path = "directory/file.txt"

        url_encoded: UrlEncoded = self._storage_url.encode(
            url=Url(
                UrlSchema.HTTP,
                "www.my-domain.com",
                "v1/streaming/{metadata}"
            ),
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference="storage-reference"
                ) \
                .classification(Classification.INTERNAL)
                .principal(Principal("USERNAME"))
                .condition(Condition(
                    datetime=DateTimeCondition(
                        access_from=DateTime.create().to_string(),
                        access_until=DateTime.create().delta(timedelta(seconds=30)).to_string()
                    )
                ))
                .metadata({
                    "key1": "áéíóú",
                    "key2": " value2 "
                })
                .build()
        )

        assert url_encoded.schema == UrlSchema.HTTPS
        assert url_encoded.authority == "www.my-domain.com"
        assert url_encoded.path == "v1/streaming/{metadata}"
        assert url_encoded.metadata
        assert re.match(r'^[https://www.my-domain.com/v1/streaming/](.)+$', url_encoded.to_url())
        # TODO add assert to check the consistency of the URL

    @final
    @override
    def test_decode__metadata_is_empty__then_raise_exception(self) -> None:
        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.decode("")

        assert str(exc_info.value) == "metadata to decode is empty"

    @final
    @override
    def test_decode__metadata_reported_full_values__then_return_url_metadata(self) -> None:
        access_from: DateTime = DateTime.create()
        access_until: DateTime = DateTime.create().delta(timedelta(seconds=30))
        path = "directory/file.txt"
        content: bytes = self._faker.sentence(10000)
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(content).once()

        url_encoded: UrlEncoded = self._storage_url.encode(
            url=Url(
                UrlSchema.HTTP,
                "www.my-domain.com",
                "v1/streaming/{metadata}"
            ),
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference="storage-reference"
                ) \
                .classification(Classification.INTERNAL)
                .principal(Principal("USERNAME"))
                .condition(Condition(
                    datetime=DateTimeCondition(
                        access_from=access_from.to_string(),
                        access_until=access_until.to_string()
                    )
                ))
                .metadata({
                    "key1": "áéíóú",
                    "key2": " value2 "
                })
                .build()
        )

        url_metadata: UrlMetadata = self._storage_url.decode(url_encoded.metadata)
        assert url_metadata.path == path
        assert url_metadata.storage_driver_reference == "storage-reference"
        assert url_metadata.classification.value == Classification.INTERNAL.value
        assert url_metadata.principal.name == "USERNAME"
        assert url_metadata.condition.datetime.access_from == access_from.to_string()
        assert url_metadata.condition.datetime.access_until == access_until.to_string()
        assert url_metadata.metadata == {"key1": "áéíóú","key2": " value2 "}

    @final
    @override
    def test_streaming__url_metadata_file_doesnt_exists__then_raise_exception(self) -> None:
        path = "directory/file.txt"
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(False).once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.streaming(
                storage_driver=storage_driver,
                url_metadata=UrlMetadata \
                    .builder(
                        path=path,
                        storage_driver_reference=""
                    ) \
                    .build()
            )

        assert str(exc_info.value) == f"file {path} doesn't exists"

    @final
    @override
    def test_streaming__url_metadata_datetime_acces_from_in_the_future__then_raise_exception(self) -> None:
        access_from: DateTime = DateTime.create().delta(timedelta(seconds=30))
        path = "directory/file.txt"
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.streaming(
                storage_driver=storage_driver,
                url_metadata=UrlMetadata \
                    .builder(
                        path=path,
                        storage_driver_reference=""
                    ) \
                    .condition(
                        Condition(
                            datetime=DateTimeCondition(
                                access_from=access_from.to_string()
                            )
                        )
                    )
                    .build()
            )

        assert str(exc_info.value) == f"resource will be accessible from {access_from}"

    @final
    @override
    def test_streaming__url_metadata_datetime_acces_until_in_the_past__then_raise_exception(self) -> None:
        access_until: DateTime = DateTime.create().delta(timedelta(seconds=-30))
        path = "directory/file.txt"
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.streaming(
                storage_driver=storage_driver,
                url_metadata=UrlMetadata \
                    .builder(
                        path=path,
                        storage_driver_reference=""
                    ) \
                    .condition(
                        Condition(
                            datetime=DateTimeCondition(
                                access_until=access_until.to_string()
                            )
                        )
                    )
                    .build()
            )

        assert str(exc_info.value) == f"resource was accessible until {access_until}"

    @final
    @override
    def test_streaming__input_stream_is_none__then_raise_exception(self) -> None:
        path = "directory/file.txt"
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(None).once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.streaming(
                storage_driver=storage_driver,
                url_metadata=UrlMetadata \
                    .builder(
                        path=path,
                        storage_driver_reference=""
                    ) \
                    .build()
            )

        assert str(exc_info.value) == "input stream obtained is none"

    @final
    @override
    def test_streaming__default_mimetype_using_file_without_extension__then_return_url_streaming(self) -> None:
        path = "directory/file"
        content: bytes = self._faker.sentence(10000)
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        url_streaming: UrlStreaming = self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        )

        assert url_streaming.content_type == "application/octet-stream"
        assert url_streaming.data.read() == content

    @final
    @override
    def test_streaming__default_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        path = "directory/file.fake"
        content: bytes = self._faker.sentence(10000)
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        url_streaming: UrlStreaming = self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        )

        assert url_streaming.content_type == "application/octet-stream"
        assert url_streaming.data.read() == content

    @final
    @override
    def test_streaming__determined_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        path = "directory/file.txt"
        content: bytes = self._faker.sentence(10000)
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        url_streaming: UrlStreaming = self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        )

        assert url_streaming.content_type == "text/plain"
        assert url_streaming.data.read() == content

    @abstractmethod
    def _create_storage_url(self) -> T:
        """
        Provides the storage url instance

        Returns:
            T: The storage url instance for testing.
        """
