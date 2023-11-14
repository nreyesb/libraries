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
import os
from urllib.parse import urlparse
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
from toku.storage.url.core import Classification
from toku.storage.url.core import Principal
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime
from toku.storage.url.core import StorageUrlException
from toku.storage.url.verifier.api import Verification
from toku.storage.url.verifier.api import StorageUrlVerificationException

T = TypeVar("T", bound=AbstractStorageUrl)


class ValidVerification(Verification):

    def __init__(self) -> None:
        self.called = False

    @override
    def verify(self, url_metadata: UrlMetadata) -> None:
        self.called = True


class InvalidVerification(Verification):

    @override
    def verify(self, url_metadata: UrlMetadata) -> None:
        raise StorageUrlVerificationException("testing raise exception for custom verifications")


class AbstractStorageUrlTest(StorageUrlTest[T], ABC, EnforceOverrides, Generic[T]):
    """
    Provides the default implementation for test cases for any kind AbstractStorageUrl class.
    """

    DEFAULT_PATH_WITH_EXTENSION = "directory/file.txt"
    DEFAULT_PATH_WITHOUT_EXTENSION = "directory/file"
    DEFAULT_MIMETYPE = "application/octet-stream"
    DEFAULT_METADATA = {"key1": "áéíóú","key2": " value2 "}

    @abstractmethod
    def _create_storage_url(self) -> T:
        """
        Provides the storage url instance

        Returns:
            T: The storage url instance for testing.
        """

    def _get_content_from_input_stream(self, input_stream: BufferedReader) -> tuple[bytes, int]:
        """
        Get the content of an input stream using a low buffer size because
        the idea is to simulate the same behavior that a TCP/IP with HTTP
        protocol does to download an input stream.

        Args:
            input_stream (BufferedReader): The content as input stream

        Returns:
            tuple[bytes, int]: The content in bytes and the total of interaction
                               that it takes to read the input stream
        """
        buffer_size = 16  # buffer size
        content = b''
        total_interation = 0

        while True:
            total_interation += 1
            chunk: bytes = input_stream.read(buffer_size)

            if not chunk:
                break  # end of the file

            content += chunk

        return (content, total_interation)

    def _get_default_url(self) -> Url:
        """
        Gets a default URL for testing purpose.

        Returns:
            Url: The URL
        """
        return Url(
            UrlSchema.HTTPS,
            "www.my-domain.com",
            "v1/streaming/{metadata}"
        )

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
                    UrlSchema.HTTPS,
                    "",
                    "path"
                ),
                url_metadata=UrlMetadata \
                    .builder(
                        path="",
                        storage_driver_reference=""
                    ) \
                    .build()
            ) \
            .to_url()

        assert str(exc_info.value) == "authority can't be empty"

    @final
    @override
    def test_encode__url_empty_path__then_raise_exception(self) -> None:
        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.encode(
                url=Url(
                    UrlSchema.HTTPS,
                    "authority",
                    ""
                ),
                url_metadata=UrlMetadata \
                    .builder(
                        path="",
                        storage_driver_reference=""
                    ) \
                    .build()
            ) \
            .to_url()

        assert str(exc_info.value) == "path can't be empty"

    @final
    @override
    def test_encode__url_metadata_to_string_is_empty__then_raise_exception(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
        url_metadata: UrlMetadata = UrlMetadata \
            .builder(
                path=path,
                storage_driver_reference=""
            ) \
            .build()
        flexmock(self._storage_url).should_receive("_process_url_metadata").with_args(url_metadata).and_return("").once()

        with pytest.raises(StorageUrlException) as exc_info:
            self._storage_url.encode(
                url=self._get_default_url(),
                url_metadata=url_metadata
            )

        assert str(exc_info.value) == "url_metadata processed is empty"

    @final
    @override
    def test_encode__url_metadata_reported_full_values__then_return_url_encoded(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION

        url_encoded: UrlEncoded = self._storage_url.encode(
            url=self._get_default_url(),
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
                .metadata(AbstractStorageUrlTest.DEFAULT_METADATA)
                .build()
        )

        url: str = url_encoded.to_url()
        url_parsed = urlparse(url)  # to check if the URL has a valid format (url safe)

        assert url_encoded.schema.value == UrlSchema.HTTPS.value
        assert url_encoded.authority == "www.my-domain.com"
        assert url_encoded.path == "v1/streaming/{metadata}"
        assert url_encoded.metadata
        assert re.match(r'^https://www\.my-domain\.com/v1/streaming/.*$', url)
        assert url == f"{url_parsed.scheme}://{url_parsed.hostname}{url_parsed.path}"

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
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION

        url_encoded: UrlEncoded = self._storage_url.encode(
            url=self._get_default_url(),
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
                .metadata(AbstractStorageUrlTest.DEFAULT_METADATA)
                .build()
        )

        url_metadata: UrlMetadata = self._storage_url.decode(url_encoded.metadata)
        assert url_metadata.path == path
        assert url_metadata.storage_driver_reference == "storage-reference"
        assert url_metadata.classification.value == Classification.INTERNAL.value
        assert url_metadata.principal.name == "USERNAME"
        assert url_metadata.condition.datetime.access_from == access_from.to_string()
        assert url_metadata.condition.datetime.access_until == access_until.to_string()
        assert url_metadata.metadata == AbstractStorageUrlTest.DEFAULT_METADATA

    @final
    @override
    def test_streaming__url_metadata_file_doesnt_exists__then_raise_exception(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
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
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
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

        assert str(exc_info.value) == f"resource will be accessible from {access_from.to_string()}"

    @final
    @override
    def test_streaming__url_metadata_datetime_acces_until_in_the_past__then_raise_exception(self) -> None:
        access_until: DateTime = DateTime.create().delta(timedelta(seconds=-30))
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
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

        assert str(exc_info.value) == f"resource was accessible until {access_until.to_string()}"

    @final
    @override
    def test_streaming__input_stream_is_none__then_raise_exception(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
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
    def test_streaming__check_custom_validation_is_called__then_raise_exception(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITHOUT_EXTENSION
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
                    .build(),
                verifications=[
                    InvalidVerification()
                ]
            )

        assert str(exc_info.value) == "testing raise exception for custom verifications"

    @final
    @override
    def test_streaming__check_custom_validation_is_called__then_return_url_streaming(self) -> None:
        verification: ValidVerification = ValidVerification()
        assert not verification.called

        path = AbstractStorageUrlTest.DEFAULT_PATH_WITHOUT_EXTENSION
        content: bytes = bytes(self._faker.sentence(10000), "UTF-8")
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        with self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build(),
            verifications=[
                verification
            ]
        ) as url_streaming:
            content_from_input_stream, total_interation = self._get_content_from_input_stream(url_streaming.data)

            assert total_interation > 1
            assert url_streaming.name == os.path.basename(AbstractStorageUrlTest.DEFAULT_PATH_WITHOUT_EXTENSION)
            assert url_streaming.content_type == AbstractStorageUrlTest.DEFAULT_MIMETYPE
            assert content_from_input_stream == content

        assert verification.called

    @final
    @override
    def test_streaming__default_mimetype_using_file_without_extension__then_return_url_streaming(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITHOUT_EXTENSION
        content: bytes = bytes(self._faker.sentence(10000), "UTF-8")
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        with self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        ) as url_streaming:
            content_from_input_stream, total_interation = self._get_content_from_input_stream(url_streaming.data)

            assert total_interation > 1
            assert url_streaming.name == os.path.basename(AbstractStorageUrlTest.DEFAULT_PATH_WITHOUT_EXTENSION)
            assert url_streaming.content_type == AbstractStorageUrlTest.DEFAULT_MIMETYPE
            assert content_from_input_stream == content

    @final
    @override
    def test_streaming__default_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        path = "directory/file.fake"
        content: bytes = bytes(self._faker.sentence(10000), "UTF-8")
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        with self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        ) as url_streaming:
            content_from_input_stream, total_interation = self._get_content_from_input_stream(url_streaming.data)

            assert total_interation > 1
            assert url_streaming.name == os.path.basename(path)
            assert url_streaming.content_type == AbstractStorageUrlTest.DEFAULT_MIMETYPE
            assert content_from_input_stream == content

    @final
    @override
    def test_streaming__determined_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        path = AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION
        content: bytes = bytes(self._faker.sentence(10000), "UTF-8")
        storage_driver = StubStorageDriver()
        flexmock(storage_driver).should_receive("exists").with_args(path).and_return(True).once()
        flexmock(storage_driver).should_receive("get_as_input_stream").with_args(path).and_return(BufferedReader(BytesIO(content))).once()  # type: ignore[arg-type]

        with self._storage_url.streaming(
            storage_driver=storage_driver,
            url_metadata=UrlMetadata \
                .builder(
                    path=path,
                    storage_driver_reference=""
                ) \
                .build()
        ) as url_streaming:
            content_from_input_stream, total_interation = self._get_content_from_input_stream(url_streaming.data)

            assert total_interation > 1
            assert url_streaming.name == os.path.basename(AbstractStorageUrlTest.DEFAULT_PATH_WITH_EXTENSION)
            assert url_streaming.content_type == "text/plain"
            assert content_from_input_stream == content
