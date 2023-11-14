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

Module: url_router_tests.py
Author: Toku
"""
from abc import ABC, abstractmethod
from datetime import timedelta
import os
import re
from typing import Generator, Optional, final
from faker import Faker
from fastapi.testclient import TestClient
from overrides import EnforceOverrides
import pytest
from toku.storage.url.core import DateTime
from toku.storage.url.core import Classification
from src.application.main import app


class UrlRouterTest(ABC, EnforceOverrides):
    """
    Provides the url endpoint test cases.
    """

    STORAGE_DRIVER_DIRECTORY = "directory"
    STORAGE_DRIVER_PATH_WITH_EXTENSION: str = f"{STORAGE_DRIVER_DIRECTORY}/file.txt"
    STORAGE_DRIVER_PATH_WITHOUT_EXTENSION: str = f"{STORAGE_DRIVER_DIRECTORY}/file"
    STORAGE_DRIVER_MIMETYPE_DEFAULT = "application/octet-stream"

    STORAGE_URL_METADATA_DEFAULT = {"key1": "áéíóú","key2": " value2 "}

    BASE_URL_PROTOCOL = "https"
    BASE_URL_AUTHORITY = "www.my-demo.com"

    @abstractmethod
    def _initialize_test(self) -> None:
        """
        """

    @abstractmethod
    def _teardown_test(self) -> None:
        """
        """

    @abstractmethod
    def _initialize_streaming_test(self) -> None:
        """
        """

    @abstractmethod
    def _teardown_streaming_test(self) -> None:
        """
        """

    @abstractmethod
    def _get_storage_driver_reference(self) -> str:
        """
        Gets the storage driver reference to create the StorageDriver to
        get the resource.

        Returns:
            str: The storage driver reference
        """

    @final
    def _get_default_url(self) -> dict:
        """
        Gets a default URL for testing purpose.

        Returns:
            dict: The URL
        """
        return {
            "url_schema": UrlRouterTest.BASE_URL_PROTOCOL,
            "authority": UrlRouterTest.BASE_URL_AUTHORITY,
            "path": f"{self._get_endpoint_streaming()}/{{metadata}}"
        }

    @final
    def _get_endpoint_encode(self) -> str:
        """
        Gets the path for encode endpoint.

        Returns:
            str: The endpoint
        """
        return "api/v1/storage/url/encode"

    @final
    def _get_endpoint_decode(self, metadata: str) -> str:
        """
        Gets the path for decode endpoint.

        Returns:
            str: The endpoint
        """
        return f"api/v1/storage/url/decode/{metadata}"

    @final
    def _get_endpoint_streaming(self, metadata: Optional[str] = None) -> str:
        """
        Gets the path for streaming endpoint.

        Returns:
            str: The endpoint
        """
        base_url = "api/v1/storage/url/streaming"

        if metadata:
            return f"{base_url}/{metadata}"

        return base_url

    @final
    def _get_url_for_streaming(self, metadata: Optional[str] = None) -> str:
        """
        Gets the full URL to invoke the streaming endpoint.

        Args:
            metadata (Optional[str], optional): The metadata for the streaming endpoint. Defaults to None.

        Returns:
            str: The streaming URL
        """
        return f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/{self._get_endpoint_streaming(metadata)}"

    @pytest.fixture(autouse=True)
    def setup_tests(self) -> Generator[None, None, None]:
        """
        Creates the `TestClient` and the `Faker`.

        Initialize the environment for each test.

        Return the control to the test.

        Teardown the environment.

        Yields:
            Generator[None, None, None]: The setup for each test
        """
        # setup
        self._client = TestClient(
            app,
            base_url=f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}"
        )
        self._faker: Faker = Faker()
        self._initialize_test()

        # return control to the tests
        yield
        self._teardown_test()

    @pytest.fixture
    def setup_streaming_test(self) -> Generator[None, None, None]:
        """
        Creates the content for the streaming tests.

        Initialize the environment for the streaming test.

        Return the control to the test.

        Teardown the environment.

        Yields:
            Generator[None, None, None]: _description_
        """
        # setup
        self._content_with_extension: str = self._faker.sentence(10000000)  # 80MB aprox
        self._content_without_extension: str = self._faker.sentence(10000000)  # 80MB aprox
        self._initialize_streaming_test()

        # return control to the tests
        yield

        # teardown
        self._teardown_streaming_test()

    @final
    def test_encode__url_empty_authority__then_raise_exception(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": {
                    "url_schema": "https",
                    "authority": "",
                    "path": "path"
                },
                "url_metadata": {
                    "path": "",
                    "storage_driver_reference": ""
                }
            }
        )
        assert response.status_code == 500
        assert response.text == '{"detail":"authority can\'t be empty"}'

    @final
    def test_encode__url_empty_path__then_raise_exception(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": {
                    "url_schema": "https",
                    "authority": "authority",
                    "path": ""
                },
                "url_metadata": {
                    "path": "",
                    "storage_driver_reference": ""
                }
            }
        )
        assert response.status_code == 500
        assert response.text == '{"detail":"path can\'t be empty"}'

    @final
    def test_encode__url_metadata_reported_minimun_values__then_return_string(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": "reference"
                }
            }
        )
        assert response.status_code == 200
        assert re.match(f'^{re.escape(self._get_url_for_streaming())}/.*$', response.text)

    @final
    def test_encode__url_metadata_reported_full_values__then_return_string(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": "reference",
                    "classification": "internal",
                    "principal": {
                        "name": "USERNAME"
                    },
                    "condition": {
                        "datetime": {
                            "access_from": DateTime.create().to_string(),
                            "access_until": DateTime.create().delta(timedelta(seconds=30)).to_string()
                        }
                    },
                    "metadata": UrlRouterTest.STORAGE_URL_METADATA_DEFAULT
                }
            }
        )
        assert response.status_code == 200
        assert re.match(f'^{re.escape(self._get_url_for_streaming())}/.*$', response.text)

    @final
    def test_decode__metadata_reported_full_values__then_return_url_metadata(self) -> None:
        access_from: DateTime = DateTime.create()
        access_until: DateTime = DateTime.create().delta(timedelta(seconds=30))
        path = UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION

        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": "reference",
                    "classification": "internal",
                    "principal": {
                        "name": "USERNAME"
                    },
                    "condition": {
                        "datetime": {
                            "access_from": access_from.to_string(),
                            "access_until": access_until.to_string()
                        }
                    },
                    "metadata": UrlRouterTest.STORAGE_URL_METADATA_DEFAULT
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        url_metadata: dict = self._client.get(self._get_endpoint_decode(url.split("/")[-1])).json()

        assert re.match(r'^[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+-[0-9a-z]+$', url_metadata["id"])
        assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6} UTC$', url_metadata["created_at"])
        assert url_metadata["path"] == path
        assert url_metadata["storage_driver_reference"] == "reference"
        assert url_metadata["classification"] == Classification.INTERNAL.value
        assert url_metadata["principal"]["name"] == "USERNAME"
        assert url_metadata["condition"]["datetime"]["access_from"] == access_from.to_string()
        assert url_metadata["condition"]["datetime"]["access_until"] == access_until.to_string()
        assert url_metadata["metadata"] == UrlRouterTest.STORAGE_URL_METADATA_DEFAULT

    @pytest.mark.usefixtures("setup_streaming_test")
    @final
    def test_streaming__url_metadata_file_doesnt_exists__then_raise_exception(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": "not-exists",
                    "storage_driver_reference": self._get_storage_driver_reference()
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        response = self._client.get(self._get_endpoint_streaming(url.split("/")[-1]))
        assert response.status_code == 409
        assert response.text == '{"detail":"file not-exists doesn\'t exists"}'

    @pytest.mark.usefixtures("setup_streaming_test")
    @final
    def test_streaming__url_metadata_datetime_acces_from_in_the_future__then_raise_exception(self) -> None:
        access_from: DateTime = DateTime.create().delta(timedelta(seconds=30))
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": self._get_storage_driver_reference(),
                    "condition": {
                        "datetime": {
                            "access_from": access_from.to_string()
                        }
                    }
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        response = self._client.get(self._get_endpoint_streaming(url.split("/")[-1]))
        assert response.status_code == 403
        assert response.text == "{" + f"\"detail\":\"resource will be accessible from {access_from.to_string()}\"" + "}"

    @pytest.mark.usefixtures("setup_streaming_test")
    @final
    def test_streaming__url_metadata_datetime_acces_until_in_the_past__then_raise_exception(self) -> None:
        access_until: DateTime = DateTime.create().delta(timedelta(seconds=-30))
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": self._get_storage_driver_reference(),
                    "condition": {
                        "datetime": {
                            "access_until": access_until.to_string()
                        }
                    }
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        response = self._client.get(self._get_endpoint_streaming(url.split("/")[-1]))
        assert response.status_code == 403
        assert response.text == "{" + f"\"detail\":\"resource was accessible until {access_until.to_string()}\"" + "}"

    @pytest.mark.usefixtures("setup_streaming_test")
    @final
    def test_streaming__default_mimetype_using_file_without_extension__then_return_url_streaming(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITHOUT_EXTENSION,
                    "storage_driver_reference": self._get_storage_driver_reference()
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        response = self._client.get(self._get_endpoint_streaming(url.split("/")[-1]))
        assert response.status_code == 200
        assert response.headers.get("content-disposition") == 'attachment; filename="' + os.path.basename(UrlRouterTest.STORAGE_DRIVER_PATH_WITHOUT_EXTENSION) + '"'
        assert response.headers.get("content-type") == "application/octet-stream"
        assert response.text == self._content_without_extension

    @pytest.mark.usefixtures("setup_streaming_test")
    @final
    def test_streaming__determined_mimetype_using_file_with_extension__then_return_url_streaming(self) -> None:
        response = self._client.post(
            self._get_endpoint_encode(),
            json={
                "url": self._get_default_url(),
                "url_metadata": {
                    "path": UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION,
                    "storage_driver_reference": self._get_storage_driver_reference()
                }
            }
        )
        url = response.text
        assert url.startswith(f"{UrlRouterTest.BASE_URL_PROTOCOL}://{UrlRouterTest.BASE_URL_AUTHORITY}/")

        response = self._client.get(self._get_endpoint_streaming(url.split("/")[-1]))
        assert response.status_code == 200
        assert response.headers.get("content-disposition") == 'attachment; filename="' + os.path.basename(UrlRouterTest.STORAGE_DRIVER_PATH_WITH_EXTENSION) + '"'
        assert "text/plain" in response.headers.get("content-type")
        assert response.text == self._content_with_extension
