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

Module: path_sanitizer_storage_driver_decorator_tests.py
Author: Toku
"""
from io import BufferedReader, BytesIO
from dataclasses import dataclass
import pytest
from flexmock import flexmock
from faker import Faker
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.api import PathSanitizer
from toku.storage.driver.api import StorageDriver
from toku.storage.driver.api import PathSanitizerStorageDriverDecorator
from toku.storage.driver.api.storage_driver import Metadata, Size
from tests.toku.storage.driver.api.stub_storage_driver import StubStorageDriver


@dataclass
class PathHelper:
    """
    Creates the helper path to keep the `path_to_sanitize`and `path_sanitized`.
    """
    path_to_sanitize: str
    path_sanitized: str


class PathSanitizerStorageDriverDecoratorTests:
    """
    Provides test cases for PathSanitizerStorageDriverDecorator class.
    """

    FAKE = Faker()

    @pytest.fixture(params=[
        (DirectorySeparator.SLASH, DirectorySeparator.SLASH),
        (DirectorySeparator.SLASH, DirectorySeparator.BACKSLASH),
        (DirectorySeparator.BACKSLASH, DirectorySeparator.SLASH),
        (DirectorySeparator.BACKSLASH, DirectorySeparator.BACKSLASH),
    ], autouse=True)
    def setup_test(self, request: pytest.FixtureRequest) -> None:
        """
        Initialize the storage_driver, storage_driver_decorator, and sanitizer using separator_sanitized
        as the directory separator for sanitized paths.

        The `request` provides a param with the list of tuples to test all the possible combinations of directory
        separators, that way it's possible ensure that all combinations work as expected, it considers:

        1) expected separator -> /  with orignal separator -> /
        2) expected separator -> /  with orignal separator -> \\
        3) expected separator -> \\ with orignal separator -> /
        4) expected separator -> \\ with orignal separator -> \\

        First position is always the final separator expected after sanitizing the path and the
        second position is always the original separator reported into the path, for example:

        - In the case 2 the original path is:

            \\root\\folder\\file.txt

          and the final path must be:

            /root/folder/file.txt

        - In the case 3 the original path is:

            /root/folder/file.txt

          and the final path must be:

            \\root\\folder\\file.txt

        Args:
            request (FixtureRequest): The tuple with the expected and original directory separators
        """
        self._separator_sanitized: DirectorySeparator
        self._separator_to_sanitize: DirectorySeparator
        self._separator_sanitized, self._separator_to_sanitize = request.param

        self._storage_driver: StorageDriver = StubStorageDriver(self._separator_sanitized)
        flexmock(self._storage_driver).should_call("get_separator").once()
        self._storage_driver_decorator: PathSanitizerStorageDriverDecorator = PathSanitizerStorageDriverDecorator(self._storage_driver)
        self._sanitizer: PathSanitizer = self._storage_driver_decorator._sanitizer  # pylint: disable=protected-access

    def _create_path(self, path: str) -> PathHelper:
        """
        Create a path to sanitize function by replacing / and \\ in the provided path with `separator_to_sanitize`.
        Also, create a path sanitized using `separator_sanitized`.

        Args:
            path (str): The path to create

        Returns:
            PathHelper: The path to sanitize and sanitized
        """
        path_to_sanitize: str = path \
            .replace(DirectorySeparator.BACKSLASH.value, self._separator_to_sanitize.value) \
            .replace(DirectorySeparator.SLASH.value, self._separator_to_sanitize.value)
        path_sanitized: str = PathSanitizer(self._separator_sanitized).sanitize(path, True)

        return PathHelper(path_to_sanitize, path_sanitized)

    def _create_byte_array(self) -> bytes:
        """
        Create a byte array from a string.

        Returns:
            bytearray: The byte array.
        """
        return bytes(PathSanitizerStorageDriverDecoratorTests.FAKE.sentence(), "utf-8")

    def _create_input_stream(self) -> BufferedReader:
        """
        Create an input stream from a byte array (`create_byte_array`).

        Returns:
            InputStream: The input stream.
        """
        bytes_handle = BytesIO(self._create_byte_array())
        return BufferedReader(bytes_handle)  # type: ignore[arg-type]

    def test_open__verify_method_invocation__then_return_void(
            self
    ) -> None:
        # assert
        flexmock(self._storage_driver_decorator).should_call("open").once()
        flexmock(self._storage_driver).should_call("open").once()

        # prepare
        self._storage_driver_decorator.open()

    def test_close__verify_method_invocation__then_return_void(
            self
    ) -> None:
        # assert
        flexmock(self._storage_driver_decorator).should_call("close").once()
        flexmock(self._storage_driver).should_call("close").once()

        # prepare
        self._storage_driver_decorator.close()

    def test_get__verify_method_invocation__then_return_optional_array_byte(self) -> None:
        # prepare
        file: PathHelper = self._create_path("/get/file.txt/")
        result_to_return: bytes = self._create_byte_array()
        flexmock(self._storage_driver_decorator).should_call("get").with_args(file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("get").with_args(file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bytes | None = self._storage_driver_decorator.get(file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_get_as_input_stream__verify_method_invocation__then_return_optional_input_stream(self) -> None:
        # prepare
        file: PathHelper = self._create_path("/get_as_input_stream/file.txt/")
        result_to_return: BufferedReader = self._create_input_stream()
        flexmock(self._storage_driver_decorator).should_call("get_as_input_stream").with_args(file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("get_as_input_stream").with_args(file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: BufferedReader | None = self._storage_driver_decorator.get_as_input_stream(file.path_to_sanitize)

        # assert
        assert result.read() if result else BytesIO() == result_to_return.read()

    def test_exists__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        file: PathHelper = self._create_path("/exists/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("exists").with_args(file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("exists").with_args(file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.exists(file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file__byte_array_source__verify_method_invocation__then_return_optional_string(self) -> None:
        # prepare
        source: bytes = self._create_byte_array()
        directory: PathHelper = self._create_path("/1/")
        result_to_return = "abcd"
        flexmock(self._storage_driver_decorator).should_call("put_file").with_args(source, directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file").with_args(source, directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logic process
        result: str | None = self._storage_driver_decorator.put_file(source, directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file__string_source__verify_method_invocation__then_return_optional_string(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/put-file/source.txt/")
        directory: PathHelper = self._create_path("/1/")
        result_to_return = "abcd"
        flexmock(self._storage_driver_decorator).should_call("put_file").with_args(source.path_to_sanitize, directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file").with_args(source.path_sanitized, directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logic process
        result: str | None = self._storage_driver_decorator.put_file(source.path_to_sanitize, directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file__input_stream_source__verify_method_invocation__then_return_optional_string(self) -> None:
        # prepare
        source: BufferedReader = self._create_input_stream()
        directory: PathHelper = self._create_path("/1/")
        result_to_return = "abcd"
        flexmock(self._storage_driver_decorator).should_call("put_file").with_args(source, directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file").with_args(source, directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logic process
        result: str | None = self._storage_driver_decorator.put_file(source, directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file_as__byte_array_source__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: bytes = self._create_byte_array()
        file: PathHelper = self._create_path("/put-file-as-byte-array-source/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("put_file_as").with_args(source, file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file_as").with_args(source, file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.put_file_as(source, file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file_as__string_source__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/put-file-as-string-source/source.txt/")
        file: PathHelper = self._create_path("/put-file-as-string-source/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("put_file_as").with_args(source.path_to_sanitize, file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file_as").with_args(source.path_sanitized, file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.put_file_as(source.path_to_sanitize, file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_put_file_as__input_stream_source__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: BufferedReader = self._create_input_stream()
        file: PathHelper = self._create_path("/put-file-as-input-stream-source/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("put_file_as").with_args(source, file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("put_file_as").with_args(source, file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.put_file_as(source, file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_append__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: bytes = self._create_byte_array()
        file: PathHelper = self._create_path("/append/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("append").with_args(source, file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("append").with_args(source, file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.append(source, file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_copy__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/copy/source.txt/")
        target: PathHelper = self._create_path("/copy/target.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("copy").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("copy").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.copy(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_copy__another_storage_driver__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        another_storage_driver = StubStorageDriver()
        source: PathHelper = self._create_path("/copy/source.txt/")
        target: PathHelper = self._create_path("/copy/target.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("copy").with_args(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("copy").with_args(source.path_sanitized, target.path_sanitized, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.copy(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver)

        # assert
        assert result == result_to_return

    def test_move__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/move/source.txt/")
        target: PathHelper = self._create_path("/move/target.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("move").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("move").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.move(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_move__another_storage_driver__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        another_storage_driver = StubStorageDriver()
        source: PathHelper = self._create_path("/move/source.txt/")
        target: PathHelper = self._create_path("/move/target.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("move").with_args(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("move").with_args(source.path_sanitized, target.path_sanitized, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.move(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver)

        # assert
        assert result == result_to_return

    def test_delete__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        file: PathHelper = self._create_path("/delete/file.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("delete").with_args(file.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("delete").with_args(file.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file.path_to_sanitize, True).and_return(file.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.delete(file.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_rename__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/rename/source.txt/")
        target: PathHelper = self._create_path("/rename/target.txt/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("rename").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("rename").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.rename(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_files__verify_method_invocation__then_return_collection_string(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/files/")
        file1: PathHelper = self._create_path("/files/1.txt/")
        file2: PathHelper = self._create_path("/files/2.txt/")
        file3: PathHelper = self._create_path("/files/3.txt/")
        flexmock(self._storage_driver_decorator).should_call("files").with_args(directory.path_to_sanitize).and_return([file1.path_sanitized, file2.path_sanitized, file3.path_sanitized]).once()
        flexmock(self._storage_driver).should_receive("files").with_args(directory.path_sanitized).and_return([file1.path_to_sanitize, file2.path_to_sanitize, file3.path_to_sanitize]).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file1.path_to_sanitize, True).and_return(file1.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file2.path_to_sanitize, True).and_return(file2.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file3.path_to_sanitize, True).and_return(file3.path_sanitized).once()

        # logic process
        paths: list[str] = self._storage_driver_decorator.files(directory.path_to_sanitize)

        # assert
        assert paths[0] == file1.path_sanitized
        assert paths[1] == file2.path_sanitized
        assert paths[2] == file3.path_sanitized

    def test_all_files__verify_method_invocation__then_return_collection_string(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/all-files/")
        file1: PathHelper = self._create_path("/all-files/1.txt/")
        file2: PathHelper = self._create_path("/all-files/2.txt/")
        file3: PathHelper = self._create_path("/all-files/3.txt/")
        file4: PathHelper = self._create_path("/all-files/2/2.txt/")
        file5: PathHelper = self._create_path("/all-files/2/3.txt/")
        flexmock(self._storage_driver_decorator).should_call("all_files").with_args(directory.path_to_sanitize).and_return([file1.path_sanitized, file2.path_sanitized, file3.path_sanitized, file4.path_sanitized, file5.path_sanitized]).once()
        flexmock(self._storage_driver).should_receive("all_files").with_args(directory.path_sanitized).and_return([file1.path_to_sanitize, file2.path_to_sanitize, file3.path_to_sanitize, file4.path_to_sanitize, file5.path_to_sanitize]).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file1.path_to_sanitize, True).and_return(file1.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file2.path_to_sanitize, True).and_return(file2.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file3.path_to_sanitize, True).and_return(file3.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file4.path_to_sanitize, True).and_return(file4.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(file5.path_to_sanitize, True).and_return(file5.path_sanitized).once()

        # logic process
        paths: list[str] = self._storage_driver_decorator.all_files(directory.path_to_sanitize)

        # assert
        assert paths[0] == file1.path_sanitized
        assert paths[1] == file2.path_sanitized
        assert paths[2] == file3.path_sanitized
        assert paths[3] == file4.path_sanitized
        assert paths[4] == file5.path_sanitized

    def test_directories__verify_method_invocation__then_return_collection_string(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/directories/")
        directory1: PathHelper = self._create_path("/directories/1/")
        directory2: PathHelper = self._create_path("/directories/2/")
        directory3: PathHelper = self._create_path("/directories/3/")
        flexmock(self._storage_driver_decorator).should_call("directories").with_args(directory.path_to_sanitize).and_return([directory1.path_sanitized, directory2.path_sanitized, directory3.path_sanitized]).once()
        flexmock(self._storage_driver).should_receive("directories").with_args(directory.path_sanitized).and_return([directory1.path_to_sanitize, directory2.path_to_sanitize, directory3.path_to_sanitize]).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory1.path_to_sanitize, True).and_return(directory1.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory2.path_to_sanitize, True).and_return(directory2.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory3.path_to_sanitize, True).and_return(directory3.path_sanitized).once()

        # logic process
        paths: list[str] = self._storage_driver_decorator.directories(directory.path_to_sanitize)

        # assert
        assert paths[0] == directory1.path_sanitized
        assert paths[1] == directory2.path_sanitized
        assert paths[2] == directory3.path_sanitized

    def test_all_directories__verify_method_invocation__then_return_collection_string(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/all-directories/")
        directory1: PathHelper = self._create_path("/all-directories/1/")
        directory2: PathHelper = self._create_path("/all-directories/2/")
        directory3: PathHelper = self._create_path("/all-directories/3/")
        directory4: PathHelper = self._create_path("/all-directories/2/2/")
        directory5: PathHelper = self._create_path("/all-directories/2/3/")
        flexmock(self._storage_driver_decorator).should_call("all_directories").with_args(directory.path_to_sanitize).and_return([directory1.path_sanitized, directory2.path_sanitized, directory3.path_sanitized, directory4.path_sanitized, directory5.path_sanitized]).once()
        flexmock(self._storage_driver).should_receive("all_directories").with_args(directory.path_sanitized).and_return([directory1.path_to_sanitize, directory2.path_to_sanitize, directory3.path_to_sanitize, directory4.path_to_sanitize, directory5.path_to_sanitize]).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory1.path_to_sanitize, True).and_return(directory1.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory2.path_to_sanitize, True).and_return(directory2.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory3.path_to_sanitize, True).and_return(directory3.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory4.path_to_sanitize, True).and_return(directory4.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory5.path_to_sanitize, True).and_return(directory5.path_sanitized).once()

        # logic process
        paths: list[str] = self._storage_driver_decorator.all_directories(directory.path_to_sanitize)

        # assert
        assert paths[0] == directory1.path_sanitized
        assert paths[1] == directory2.path_sanitized
        assert paths[2] == directory3.path_sanitized
        assert paths[3] == directory4.path_sanitized
        assert paths[4] == directory5.path_sanitized

    def test_exists_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/exists-directory/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("exists_directory").with_args(directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("exists_directory").with_args(directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.exists_directory(directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_copy_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/copy-directory/source/")
        target: PathHelper = self._create_path("/copy-directory/target/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("copy_directory").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("copy_directory").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.copy_directory(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_copy_directory__another_storage_driver__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        another_storage_driver = StubStorageDriver()
        source: PathHelper = self._create_path("/copy-directory/source/")
        target: PathHelper = self._create_path("/copy-directory/target/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("copy_directory").with_args(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("copy_directory").with_args(source.path_sanitized, target.path_sanitized, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.copy_directory(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver)

        # assert
        assert result == result_to_return

    def test_move_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/move-directory/source/")
        target: PathHelper = self._create_path("/move-directory/target/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("move_directory").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("move_directory").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.move_directory(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_move_directory__another_storage_driver__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        another_storage_driver = StubStorageDriver()
        source: PathHelper = self._create_path("/move-directory/source/")
        target: PathHelper = self._create_path("/move-directory/target/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("move_directory").with_args(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("move_directory").with_args(source.path_sanitized, target.path_sanitized, another_storage_driver).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.move_directory(source.path_to_sanitize, target.path_to_sanitize, another_storage_driver)

        # assert
        assert result == result_to_return

    def test_make_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/make-directory/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("make_directory").with_args(directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("make_directory").with_args(directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logi: boolc process
        result: bool = self._storage_driver_decorator.make_directory(directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_delete_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        directory: PathHelper = self._create_path("/delete-directory/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("delete_directory").with_args(directory.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("delete_directory").with_args(directory.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(directory.path_to_sanitize, True).and_return(directory.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.delete_directory(directory.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_rename_directory__verify_method_invocation__then_return_boolean(self) -> None:
        # prepare
        source: PathHelper = self._create_path("/rename-directory/source/")
        target: PathHelper = self._create_path("/rename-directory/target/")
        result_to_return = True
        flexmock(self._storage_driver_decorator).should_call("rename_directory").with_args(source.path_to_sanitize, target.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("rename_directory").with_args(source.path_sanitized, target.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(source.path_to_sanitize, True).and_return(source.path_sanitized).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(target.path_to_sanitize, True).and_return(target.path_sanitized).once()

        # logic process
        result: bool = self._storage_driver_decorator.rename_directory(source.path_to_sanitize, target.path_to_sanitize)

        # assert
        assert result == result_to_return


    def test_get_metadata__verify_method_invocation__then_return_optional_metadata(self) -> None:
        # prepare
        path: PathHelper = self._create_path("/metadata/path/")
        result_to_return = Metadata(Size(100), 100, 100, 100, False, False, False, "")
        flexmock(self._storage_driver_decorator).should_call("get_metadata").with_args(path.path_to_sanitize).and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("get_metadata").with_args(path.path_sanitized).and_return(result_to_return).once()
        flexmock(self._sanitizer).should_call("sanitize").with_args(path.path_to_sanitize, True).and_return(path.path_sanitized).once()

        # logic process
        result: Metadata | None = self._storage_driver_decorator.get_metadata(path.path_to_sanitize)

        # assert
        assert result == result_to_return

    def test_get_root__verify_method_invocation__then_return_string(self) -> None:
        # prepare
        result_to_return = "/root"
        flexmock(self._storage_driver_decorator).should_call("get_root").and_return(result_to_return).once()
        flexmock(self._storage_driver).should_receive("get_root").and_return(result_to_return).once()

        # logic process
        result: str = self._storage_driver_decorator.get_root()

        # assert
        assert result == result_to_return
