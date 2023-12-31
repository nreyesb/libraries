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

Module: abstract_storage_driver_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from io import BufferedReader, BytesIO
import os
import tempfile
from typing import Generator, Generic, Optional, TypeVar, final
from dataclasses import dataclass
import humanize
from overrides import EnforceOverrides, override
import pytest
from faker import Faker
from tests.toku.storage.driver.api import StorageDriverTest
from toku.storage.driver.api import Metadata
from toku.storage.driver.api import PathSanitizer
from toku.storage.driver.api import AbstractStorageDriver
from toku.storage.driver.api import StorageDriverException

T = TypeVar("T", bound=AbstractStorageDriver)


@dataclass
class FileCreatorData:
    """
    Helper class to keep all the relevant information of data created for testing
    """
    path: str
    content: bytes


class AbstractStorageDriverTest(StorageDriverTest[T], ABC, EnforceOverrides, Generic[T]):
    """
    Provides the default implementation for test cases for any kind AbstractStorageDriver class.
    """

    @final
    def _create_string(self, words: Optional[int] = 20 ) -> str:
        """
        Create a random string.

        Args:
            words (Optional[int]): Total of words. Defaults to 20.

        Returns:
            bytearray: The byte array.
        """
        return f"{self._faker.sentence(words)}"

    @final
    def _create_byte_array(self) -> bytes:
        """
        Create a byte array from a string.

        Returns:
            bytearray: The byte array.
        """
        return bytes(self._create_string(), "utf-8")

    @final
    def _create_input_stream(self, content: Optional[bytes] = None) -> BufferedReader:
        """
        Create an input stream from a byte array.

        Args:
            content (Optional[bytes]): The content. Defaults to None.

        Returns:
            InputStream: The input stream.
        """
        bytes_handle = BytesIO(content if content else self._create_byte_array())
        return BufferedReader(bytes_handle)  # type: ignore[arg-type]

    @final
    def _create_file_in_local(
            self,
            directory: str,
            name: str
    ) -> FileCreatorData:
        """
        Create a file giving the `directory` and `name` in the local machine.

        The content is a random sentence.

        Args:
            directory (str): The directory name
            name (str): The filename

        Returns:
            FileCreatorData: The file creator data
        """
        temp_file: str = os.path.join(self._tempdir.name, directory, name)
        content: bytes = self._create_byte_array()

        with open(temp_file, "wb") as file:
            file.write(content)

        return FileCreatorData(temp_file, content)

    @final
    def _create_file_in_storage_driver(
            self,
            directory: Optional[str],
            name: str,
            target_storage_driver: Optional[T] = None
    ) -> FileCreatorData:
        """
        Create a file giving the `directory` and `name` in the `target_storage_driver`
        or in the `self.storage_driver` if the `target_storage_driver` is None.

        The content is a random sentence.

        Args:
            directory (Optional[str]): The directory name
            name (str): The filename
            target_storage_driver (Optional[T]): The storage driver to use. Defaults to None.

        Returns:
            FileCreatorData: The file creator data
        """
        storage_driver: T = self._storage_driver if not target_storage_driver else target_storage_driver
        path: str = name if not directory or not directory.strip() else self._sanitizer.concat(directory, name)
        content: bytes = bytes(self._faker.sentence(), "UTF-8")
        if not storage_driver.put_file_as(content, path):
            raise StorageDriverException(f"Could not create the file {path} for testing purpose")

        return FileCreatorData(path, content)

    @final
    def _create_directory_in_storage_driver(
            self,
            directory: str,
            target_storage_driver: Optional[T] = None
    ) -> str:
        """
        Create a empty directory giving the `directory` `target_storage_driver`
        or in the `self.storage_driver` if the `target_storage_driver` is None.

        Args:
            directory (str): The directory name
            target_storage_driver (Optional[T]): The storage driver to use. Defaults to None.

        Returns:
            str: The directory name
        """
        storage_driver: T = self._storage_driver if not target_storage_driver else target_storage_driver
        directory = self._sanitizer.sanitize(directory)

        if not storage_driver.make_directory(directory):
            raise StorageDriverException(f"Could not create the directory {directory} for testing purpose")

        return directory

    @abstractmethod
    def _create_storage_driver(self) -> T:
        """
        Provides the storage driver instance

        Returns:
            T: The storage driver instance for testing.
        """

    @abstractmethod
    def _create_storage_driver_secondary(self) -> T:
        """
        Provides the storage driver secondary instance

        Returns:
            T: The storage driver secondary instance for testing.
        """

    @final
    @pytest.fixture(autouse=True)
    def setup_test(self) -> Generator[None, None, None]:
        """
        Start the temporary directory

        Start the setup process (sub-class).

        Initialize the `storage_driver` by opening, the `sanitizer` and the `faker`.

        Return the control to the test.

        Cleanup the temporary directory.

        Close the `storage_driver`.

        Start the teardown process (sub-class).

        Yields:
            Generator[None, None, None]: To return the control to the test and after that finishing the test
        """
        # setup
        self._tempdir = tempfile.TemporaryDirectory()
        self._initialize_test()
        self._storage_driver: T = self._create_storage_driver()
        self._storage_driver.open()
        self._sanitizer: PathSanitizer = PathSanitizer(self._storage_driver.get_separator())
        self._faker = Faker()

        # return control to the test
        yield

        # teardown
        self._tempdir.cleanup()
        self._storage_driver.close()
        self._teardown_test()

    @final
    @override
    def test_get__file_not_exists__then_return_optional_none(self) -> None:
        assert not self._storage_driver.exists("file-not-exists.txt")
        assert self._storage_driver.get("file-not-exists.txt") is None

    @final
    @override
    def test_get__file_is_directory__then_return_optional_none(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.get("directory") is None

    @final
    @override
    def test_get__file_is_root__then_return_optional_none(self) -> None:
        assert self._storage_driver.get("") is None
        assert self._storage_driver.get("    ") is None

    @final
    @override
    def test_get__file_in_directory__then_return_optional_byte_array(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")
        assert file_creator_data.path == self._sanitizer.sanitize("directory/file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.get(file_creator_data.path) == file_creator_data.content

    @final
    @override
    def test_get__file_in_root__then_return_optional_byte_array(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert file_creator_data.path == "file.txt"
        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.get(file_creator_data.path) == file_creator_data.content

    @final
    @override
    def test_get_as_input_stream__file_not_exists__then_return_optional_none(self) -> None:
        assert not self._storage_driver.exists("file.txt")
        assert self._storage_driver.get_as_input_stream("file.txt") is None

    @final
    @override
    def test_get_as_input_stream__file_is_directory__then_return_optional_none(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.get_as_input_stream("directory") is None

    @final
    @override
    def test_get_as_input_stream__file_is_root__then_return_optional_none(self) -> None:
        assert self._storage_driver.get_as_input_stream("") is None
        assert self._storage_driver.get_as_input_stream("    ") is None

    @final
    @override
    def test_get_as_input_stream__file_in_directory__then_return_optional_input_stream(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")
        assert file_creator_data.path == self._sanitizer.sanitize("directory/file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        is_: Optional[BufferedReader] = self._storage_driver.get_as_input_stream(file_creator_data.path)
        if is_:
            with is_:
                assert is_.read() == file_creator_data.content

    @final
    @override
    def test_get_as_input_stream__file_in_root__then_return_optional_input_stream(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert file_creator_data.path == "file.txt"
        assert self._storage_driver.exists(file_creator_data.path)
        is_: Optional[BufferedReader] = self._storage_driver.get_as_input_stream(file_creator_data.path)
        if is_:
            with is_:
                assert is_.read() == file_creator_data.content

    @final
    @override
    def test_exists__file_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("file.txt")
        assert not self._storage_driver.exists("file.txt")

    @final
    @override
    def test_exists__file_is_directory__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("directory")

    @final
    @override
    def test_exists__file_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.exists("")
        assert not self._storage_driver.exists("    ")

    @final
    @override
    def test_exists__file_in_directory__then_return_true(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")
        assert file_creator_data.path == self._sanitizer.sanitize("directory/file.txt")
        assert self._storage_driver.exists(file_creator_data.path)

    @final
    @override
    def test_exists__file_in_root__then_return_true(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert file_creator_data.path == "file.txt"
        assert self._storage_driver.exists(file_creator_data.path)

    @final
    @override
    def test_put_file__byte_array__file_in_existing_file__then_return_optional_none(self) -> None:
        content: bytes = self._create_byte_array()
        name: Optional[str] = None
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert len(self._storage_driver.files("")) == 1
        name = self._storage_driver.put_file(content, file_creator_data.path)
        assert not name
        assert len(self._storage_driver.files("")) == 1

    @final
    @override
    def test_put_file__byte_array__file_in_directory__then_return_optional_string(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"
        content1: bytes = self._create_byte_array()
        content2: bytes = self._create_byte_array()
        name: Optional[str] = ""

        # directory 1
        name = self._storage_driver.put_file(content1, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == content1

        name = self._storage_driver.put_file(content1, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == content1

        # directory 2
        name = self._storage_driver.put_file(content2, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == content2

        name = self._storage_driver.put_file(content2, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == content2

    @final
    @override
    def test_put_file__byte_array__file_in_root__then_return_optional_string(self) -> None:
        content: bytes = self._create_byte_array()
        name: Optional[str] = ""

        assert len(self._storage_driver.files("")) == 0
        name = self._storage_driver.put_file(content, "")
        assert name and len(name) > 16
        name = self._storage_driver.put_file(content, "")
        assert name and len(name) > 16
        name = self._storage_driver.put_file(content, "    ")
        assert name and len(name) > 16
        assert len(self._storage_driver.files("")) == 3

    @final
    @override
    def test_put_file__input_stream__file_in_existing_file__then_return_optional_none(self) -> None:
        array: bytes = self._create_byte_array()
        content: BufferedReader = self._create_input_stream(array)

        name: Optional[str] = None

        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert len(self._storage_driver.files("")) == 1
        name = self._storage_driver.put_file(content, file_creator_data.path)
        assert not name
        assert len(self._storage_driver.files("")) == 1

    @final
    @override
    def test_put_file__input_stream__file_in_directory__then_return_optional_string(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"

        array1: bytes = self._create_byte_array()
        array2: bytes = self._create_byte_array()
        content1: BufferedReader = self._create_input_stream(array1)
        content2: BufferedReader = self._create_input_stream(array2)

        name: Optional[str] = ""

        # directory 1
        name = self._storage_driver.put_file(content1, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == array1

        content1.seek(0)
        name = self._storage_driver.put_file(content1, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == array1

        # directory 2
        name = self._storage_driver.put_file(content2, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == array2

        content2.seek(0)
        name = self._storage_driver.put_file(content2, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == array2

    @final
    @override
    def test_put_file__input_stream__file_in_root__then_return_optional_string(self) -> None:
        array1: bytes = self._create_byte_array()
        array2: bytes = self._create_byte_array()
        array3: bytes = self._create_byte_array()
        content1: BufferedReader = self._create_input_stream(array1)
        content2: BufferedReader = self._create_input_stream(array2)
        content3: BufferedReader = self._create_input_stream(array3)

        name: Optional[str] = None

        assert len(self._storage_driver.files("")) == 0
        name = self._storage_driver.put_file(content1, "")
        assert name and len(name) > 16
        name = self._storage_driver.put_file(content2, "")
        assert name and len(name) > 16
        name = self._storage_driver.put_file(content3, "    ")
        assert name and len(name) > 16
        assert len(self._storage_driver.files("")) == 3

    @final
    @override
    def test_put_file__path_as_string__file_in_existing_file__then_return_optional_none(self) -> None:
        content: str = self._create_file_in_local("", "file1").path

        name: Optional[str] = None

        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(None, "file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert len(self._storage_driver.files("")) == 1
        name = self._storage_driver.put_file(content, file_creator_data.path)
        assert name is None or name == ""
        assert len(self._storage_driver.files("")) == 1

    @final
    @override
    def test_put_file__path_as_string__file_in_directory__then_return_optional_string(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"

        content1: FileCreatorData = self._create_file_in_local("", "file1")
        content2: FileCreatorData = self._create_file_in_local("", "file2")

        name: Optional[str] = None

        # directory 1
        name = self._storage_driver.put_file(content1.path, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == content1.content

        name = self._storage_driver.put_file(content1.path, directory1)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory1)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory1, name)) == content1.content

        # directory 2
        name = self._storage_driver.put_file(content2.path, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == content2.content

        name = self._storage_driver.put_file(content2.path, directory2)
        assert name and len(name) > 16
        assert len(self._storage_driver.files(directory2)) == 2
        assert self._storage_driver.get(self._sanitizer.concat(directory2, name)) == content2.content

    @final
    @override
    def test_put_file__path_as_string__file_in_root__then_return_optional_string(self) -> None:
        content: str = self._create_file_in_local("", "file1").path

        name: Optional[str] = None

        assert len(self._storage_driver.files("")) == 0
        name = self._storage_driver.put_file(content, "")
        assert name and len(name) > 16
        name = self._storage_driver.put_file(content, "    ")
        assert name and len(name) > 16
        assert len(self._storage_driver.files("")) == 2

    @final
    @override
    def test_put_file_as__byte_array__file_in_directory__then_return_true(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"

        content1: bytes = self._create_byte_array()
        content2: bytes = self._create_byte_array()

        file1: str = self._sanitizer.concat(directory1, "file1.txt")
        file2: str = self._sanitizer.concat(directory2, "file2.txt")

        # directory 1
        assert self._storage_driver.put_file_as(content1, file1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(file1) == content1

        assert self._storage_driver.put_file_as(content2, file1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(file1) == content2

        # directory 2
        assert self._storage_driver.put_file_as(content2, file2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(file2) == content2

        assert self._storage_driver.put_file_as(content1, file2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(file2) == content1

    @final
    @override
    def test_put_file_as__byte_array__file_in_root__then_return_true(self) -> None:
        content: bytes = self._create_byte_array()

        assert len(self._storage_driver.files("")) == 0
        assert self._storage_driver.put_file_as(content, "file1.txt")
        assert self._storage_driver.put_file_as(content, "file2.txt")
        assert self._storage_driver.put_file_as(content, "    file3.txt")
        assert len(self._storage_driver.files("")) == 3

    @final
    @override
    def test_put_file_as__byte_array__file_in_existing_file_as_directory__then_return_false(self) -> None:
        directory: str = "directory1"
        content: bytes = self._create_byte_array()
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(directory, "file1.txt")

        assert not self._storage_driver.put_file_as(content, self._sanitizer.concat(file_creator_data.path, "file2.txt"))
        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.exists(self._sanitizer.concat(file_creator_data.path, "file2.txt"))

    @final
    @override
    def test_put_file_as__byte_array__file_without_name__then_return_false(self) -> None:
        content: bytes = self._create_byte_array()

        assert self._storage_driver.make_directory("directory")
        assert not self._storage_driver.put_file_as(content, "directory")
        assert not self._storage_driver.put_file_as(content, "")
        assert not self._storage_driver.put_file_as(content, "    ")
        assert len(self._storage_driver.files("")) == 0

    @final
    @override
    def test_put_file_as__input_stream__file_in_directory__then_return_true(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"
        array1: bytes = self._create_byte_array()
        array2: bytes = self._create_byte_array()
        content1: BufferedReader = self._create_input_stream(array1)
        content2: BufferedReader = self._create_input_stream(array2)
        file1: str = self._sanitizer.concat(directory1, "file1.txt")
        file2: str = self._sanitizer.concat(directory2, "file2.txt")

        # directory 1
        assert self._storage_driver.put_file_as(content1, file1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(file1) == array1

        assert self._storage_driver.put_file_as(content2, file1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(file1) == array2

        # directory 2
        content2.seek(0)
        assert self._storage_driver.put_file_as(content2, file2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(file2) == array2

        content1.seek(0)
        assert self._storage_driver.put_file_as(content1, file2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(file2) == array1

    @final
    @override
    def test_put_file_as__input_stream__file_in_root__then_return_true(self) -> None:
        array1: bytes = self._create_byte_array()
        array2: bytes = self._create_byte_array()
        array3: bytes = self._create_byte_array()
        content1: BufferedReader = self._create_input_stream(array1)
        content2: BufferedReader = self._create_input_stream(array2)
        content3: BufferedReader = self._create_input_stream(array3)

        assert len(self._storage_driver.files("")) == 0
        assert self._storage_driver.put_file_as(content1, "file1.txt")
        assert self._storage_driver.put_file_as(content2, "file2.txt")
        assert self._storage_driver.put_file_as(content3, "    file3.txt")
        assert len(self._storage_driver.files("")) == 3

    @final
    @override
    def test_put_file_as__input_stream__file_in_existing_file_as_directory__then_return_false(self) -> None:
        directory: str = "directory1"
        array: bytes = self._create_byte_array()
        content: BufferedReader = self._create_input_stream(array)
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(directory, "file1.txt")

        assert not self._storage_driver.put_file_as(content, self._sanitizer.concat(file_creator_data.path, "file2.txt"))
        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.exists(self._sanitizer.concat(file_creator_data.path, "file2.txt"))

    @final
    @override
    def test_put_file_as__input_stream__file_without_name__then_return_false(self) -> None:
        array: bytes = self._create_byte_array()
        content: BufferedReader = self._create_input_stream(array)

        assert self._storage_driver.make_directory("directory")
        assert not self._storage_driver.put_file_as(content, "directory")
        assert not self._storage_driver.put_file_as(content, "")
        assert not self._storage_driver.put_file_as(content, "    ")
        assert len(self._storage_driver.files("")) == 0

    @final
    @override
    def test_put_file_as__path_as_string__file_in_directory__then_return_true(self) -> None:
        directory1: str = "directory1"
        directory2: str = "directory2"
        content1: FileCreatorData = self._create_file_in_local("", "file1")
        content2: FileCreatorData = self._create_file_in_local("", "file2")
        path1: str = self._sanitizer.concat(directory1, "file1.txt")
        path2: str = self._sanitizer.concat(directory2, "file2.txt")

        # directory 1
        assert self._storage_driver.put_file_as(content1.path, path1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(path1) == content1.content

        assert self._storage_driver.put_file_as(content2.path, path1)
        assert len(self._storage_driver.files(directory1)) == 1
        assert self._storage_driver.get(path1) == content2.content

        # directory 2
        assert self._storage_driver.put_file_as(content2.path, path2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(path2) == content2.content

        assert self._storage_driver.put_file_as(content1.path, path2)
        assert len(self._storage_driver.files(directory2)) == 1
        assert self._storage_driver.get(path2) == content1.content

    @final
    @override
    def test_put_file_as__path_as_string__file_in_root__then_return_true(self) -> None:
        content: str = self._create_file_in_local("", "file").path

        assert len(self._storage_driver.files("")) == 0
        assert self._storage_driver.put_file_as(content, "file1.txt")
        assert self._storage_driver.put_file_as(content, "file2.txt")
        assert self._storage_driver.put_file_as(content, "    file3.txt")
        assert len(self._storage_driver.files("")) == 3

    @final
    @override
    def test_put_file_as__path_as_string__file_in_existing_file_as_directory__then_return_false(self) -> None:
        directory: str = "directory1"
        content: str = self._create_file_in_local("", "file1").path
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver(directory, "file1.txt")

        assert not self._storage_driver.put_file_as(content, self._sanitizer.concat(file_creator_data.path, "file2.txt"))
        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.exists(self._sanitizer.concat(file_creator_data.path, "file2.txt"))

    @final
    @override
    def test_put_file_as__path_as_string__file_without_name__then_return_false(self) -> None:
        content: str = self._create_file_in_local("", "file").path

        assert self._storage_driver.make_directory("directory")
        assert not self._storage_driver.put_file_as(content, "directory")
        assert not self._storage_driver.put_file_as(content, "")
        assert not self._storage_driver.put_file_as(content, "    ")
        assert len(self._storage_driver.files("")) == 0

    @final
    @override
    def test_append__file_not_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))
        assert not self._storage_driver.append(self._create_byte_array(), "file.txt")
        assert not self._storage_driver.append(self._create_byte_array(), self._sanitizer.sanitize("directory/file.txt"))

    @final
    @override
    def test_append__file_is_directory__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.append(self._create_byte_array(), "directory")

    @final
    @override
    def test_append__file_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.append(self._create_byte_array(), "")
        assert not self._storage_driver.append(self._create_byte_array(), "    ")

    @final
    @override
    def test_append__file_in_directory__then_return_true(self) -> None:
        directory: str = "directory"
        file: str = "file.txt"
        original: str = self._create_string()
        append: str = self._create_string()

        assert self._storage_driver.put_file_as(original.encode("UTF-8"), self._sanitizer.concat(directory, file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, file))
        assert self._storage_driver.append(append.encode("UTF-8"), self._sanitizer.concat(directory, file))
        assert self._storage_driver.get(self._sanitizer.concat(directory, file)) == bytes(f"{original}{append}", "utf-8")

    @final
    @override
    def test_append__file_in_root__then_return_true(self) -> None:
        file: str = "file.txt"
        original: str = self._create_string()
        append: str = self._create_string()

        assert self._storage_driver.put_file_as(original.encode("UTF-8"), file)
        assert self._storage_driver.exists(file)
        assert self._storage_driver.append(append.encode("UTF-8"), file)
        assert self._storage_driver.get(file) == bytes(f"{original}{append}", "utf-8")

    @final
    @override
    def test_copy__source_not_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.copy("file.tx", "file1.txt")
        assert not self._storage_driver.copy(self._sanitizer.sanitize("directory/file.txt"), "file2.txt")

    @final
    @override
    def test_copy__source_is_directory__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.copy("directory", "file1.txt")
        assert not self._storage_driver.copy("directory", "file2.txt")

    @final
    @override
    def test_copy__source_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.exists("file3.txt")
        assert not self._storage_driver.copy("", "file2.txt")
        assert not self._storage_driver.copy("    ", "file3.txt")

    @final
    @override
    def test_copy__target_is_directory__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory")

        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.copy(file_creator_data.path, directory)

    @final
    @override
    def test_copy__target_is_root__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.copy(file_creator_data.path, "")
        assert not self._storage_driver.copy(file_creator_data.path, "    ")

    @final
    @override
    def test_copy__source_exists_and_target_is_source__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.copy(file_creator_data.path, file_creator_data.path)

    @final
    @override
    def test_copy__target_not_exists__then_return_true(self) -> None:
        directory: str = "directory"
        original_file: str = "file.txt"
        copy_file: str = "copy.txt"
        content: bytes = self._create_byte_array()

        assert self._storage_driver.put_file_as(content, self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert not self._storage_driver.exists(self._sanitizer.concat(directory, copy_file))
        assert not self._storage_driver.exists(copy_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
        assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), copy_file)
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.exists(copy_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
        assert self._storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content
        assert self._storage_driver.get(copy_file) == content

    @final
    @override
    def test_copy__target_is_file__then_return_true(self) -> None:
        directory: str = "directory"
        original_file: str = "file.txt"
        copy_file: str = "copy.txt"
        content1: bytes = self._create_byte_array()
        content2: bytes = self._create_byte_array()
        content3: bytes = self._create_byte_array()

        assert self._storage_driver.put_file_as(content1, self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.put_file_as(content2, self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.put_file_as(content3, copy_file)
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.exists(copy_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
        assert self._storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content2
        assert self._storage_driver.get(copy_file) == content3
        assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), copy_file)
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, copy_file))
        assert self._storage_driver.exists(copy_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
        assert self._storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content1
        assert self._storage_driver.get(copy_file) == content1

    @final
    @override
    def test_copy__another_storage_driver__target_is_directory__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
            directory: str = self._create_directory_in_storage_driver("directory", target_storage_driver)

            assert self._storage_driver.exists(file_creator_data.path)
            assert target_storage_driver.exists_directory(directory)
            assert not self._storage_driver.copy(file_creator_data.path, directory, target_storage_driver)

    @final
    @override
    def test_copy__another_storage_driver__target_is_root__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

            assert self._storage_driver.exists(file_creator_data.path)
            assert not self._storage_driver.copy(file_creator_data.path, "", target_storage_driver)
            assert not self._storage_driver.copy(file_creator_data.path, "    ", target_storage_driver)

    @final
    @override
    def test_copy__another_storage_driver__source_exists_and_target_is_source__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

            assert self._storage_driver.exists(file_creator_data.path)
            assert self._storage_driver.copy(file_creator_data.path, file_creator_data.path, target_storage_driver)

    @final
    @override
    def test_copy__another_storage_driver__target_not_exists__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory: str = "directory"
            original_file: str = "file.txt"
            copy_file: str = "copy.txt"
            content: bytes = self._create_byte_array()

            assert self._storage_driver.put_file_as(content, self._sanitizer.concat(directory, original_file))
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert not target_storage_driver.exists(self._sanitizer.concat(directory, copy_file))
            assert not target_storage_driver.exists(copy_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
            assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, copy_file), target_storage_driver)
            assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), copy_file, target_storage_driver)
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, copy_file))
            assert target_storage_driver.exists(copy_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
            assert target_storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content
            assert target_storage_driver.get(copy_file) == content

    @final
    @override
    def test_copy__another_storage_driver__target_is_file__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory: str = "directory"
            original_file: str = "file.txt"
            copy_file: str = "copy.txt"
            content1: bytes = self._create_byte_array()
            content2: bytes = self._create_byte_array()
            content3: bytes = self._create_byte_array()

            assert self._storage_driver.put_file_as(content1, self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.put_file_as(content2, self._sanitizer.concat(directory, copy_file))
            assert target_storage_driver.put_file_as(content3, copy_file)
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, copy_file))
            assert target_storage_driver.exists(copy_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
            assert target_storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content2
            assert target_storage_driver.get(copy_file) == content3
            assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file),
                                            self._sanitizer.concat(directory, copy_file), target_storage_driver)
            assert self._storage_driver.copy(self._sanitizer.concat(directory, original_file), copy_file, target_storage_driver)
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, copy_file))
            assert target_storage_driver.exists(copy_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
            assert target_storage_driver.get(self._sanitizer.concat(directory, copy_file)) == content1
            assert target_storage_driver.get(copy_file) == content1

    @final
    @override
    def test_move__source_not_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.move("file.tx", "file2.txt")
        assert not self._storage_driver.move(self._sanitizer.sanitize("directory/file.txt"), "file2.txt")

    @final
    @override
    def test_move__source_is_directory__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.move("directory", "file2.txt")
        assert not self._storage_driver.move("directory", "file1.txt")

    @final
    @override
    def test_move__source_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.exists("file1.txt")
        assert not self._storage_driver.exists("file2.txt")
        assert not self._storage_driver.exists("file3.txt")
        assert not self._storage_driver.move("", "file2.txt")
        assert not self._storage_driver.move("    ", "file3.txt")

    @final
    @override
    def test_move__target_is_directory__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory")

        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.move(file_creator_data.path, directory)

    @final
    @override
    def test_move__target_is_root__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.move(file_creator_data.path, "")
        assert not self._storage_driver.move(file_creator_data.path, "    ")

    @final
    @override
    def test_move__source_exists_and_target_is_source__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.move(file_creator_data.path, file_creator_data.path)

    @final
    @override
    def test_move__target_not_exists__then_return_true(self) -> None:
        directory: str = "directory"
        original_file: str = "file.txt"
        move_file: str = "move.txt"
        content: bytes = self._create_byte_array()

        assert self._storage_driver.put_file_as(content, self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert not self._storage_driver.exists(self._sanitizer.concat(directory, move_file))
        assert not self._storage_driver.exists(move_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
        assert self._storage_driver.move(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, move_file))
        assert not self._storage_driver.move(self._sanitizer.concat(directory, original_file), move_file)
        assert not self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, move_file))
        assert not self._storage_driver.exists(move_file)
        assert not self._storage_driver.get(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.get(self._sanitizer.concat(directory, move_file)) == content
        assert not self._storage_driver.get(move_file)

    @final
    @override
    def test_move__target_is_file__then_return_true(self) -> None:
        directory: str = "directory"
        original_file: str = "file.txt"
        move_file: str = "move.txt"
        content1: bytes = self._create_byte_array()
        content2: bytes = self._create_byte_array()
        content3: bytes = self._create_byte_array()

        assert self._storage_driver.put_file_as(content1, self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.put_file_as(content2, self._sanitizer.concat(directory, move_file))
        assert self._storage_driver.put_file_as(content3, move_file)
        assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, move_file))
        assert self._storage_driver.exists(move_file)
        assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
        assert self._storage_driver.get(self._sanitizer.concat(directory, move_file)) == content2
        assert self._storage_driver.get(move_file) == content3
        assert self._storage_driver.move(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, move_file))
        assert not self._storage_driver.move(self._sanitizer.concat(directory, original_file), move_file)
        assert not self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.exists(self._sanitizer.concat(directory, move_file))
        assert self._storage_driver.exists(move_file)
        assert not self._storage_driver.get(self._sanitizer.concat(directory, original_file))
        assert self._storage_driver.get(self._sanitizer.concat(directory, move_file)) == content1
        assert self._storage_driver.get(move_file) == content3

    @final
    @override
    def test_move__another_storage_driver__target_is_directory__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
            directory: str = self._create_directory_in_storage_driver("directory", target_storage_driver)

            assert self._storage_driver.exists(file_creator_data.path)
            assert target_storage_driver.exists_directory(directory)
            assert not self._storage_driver.move(file_creator_data.path, directory, target_storage_driver)

    @final
    @override
    def test_move__another_storage_driver__target_is_root__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

            assert self._storage_driver.exists(file_creator_data.path)
            assert not self._storage_driver.move(file_creator_data.path, "", target_storage_driver)
            assert not self._storage_driver.move(file_creator_data.path, "    ", target_storage_driver)

    @final
    @override
    def test_move__another_storage_driver__source_exists_and_target_is_source__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

            assert self._storage_driver.exists(file_creator_data.path)
            assert self._storage_driver.move(file_creator_data.path, file_creator_data.path, target_storage_driver)

    @final
    @override
    def test_move__another_storage_driver__target_not_exists__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory: str = "directory"
            original_file: str = "file.txt"
            move_file: str = "move.txt"
            content: bytes = self._create_byte_array()

            assert self._storage_driver.put_file_as(content, self._sanitizer.concat(directory, original_file))
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert not target_storage_driver.exists(self._sanitizer.concat(directory, move_file))
            assert not target_storage_driver.exists(move_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content
            assert self._storage_driver.move(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, move_file), target_storage_driver)
            assert not self._storage_driver.move(self._sanitizer.concat(directory, original_file), move_file, target_storage_driver)
            assert not self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, move_file))
            assert not target_storage_driver.exists(move_file)
            assert not self._storage_driver.get(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.get(self._sanitizer.concat(directory, move_file)) == content
            assert not target_storage_driver.get(move_file)

    @final
    @override
    def test_move__another_storage_driver__target_is_file__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory: str = "directory"
            original_file: str = "file.txt"
            move_file: str = "move.txt"
            content1: bytes = self._create_byte_array()
            content2: bytes = self._create_byte_array()
            content3: bytes = self._create_byte_array()

            assert self._storage_driver.put_file_as(content1, self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.put_file_as(content2, self._sanitizer.concat(directory, move_file))
            assert target_storage_driver.put_file_as(content3, move_file)
            assert self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, move_file))
            assert target_storage_driver.exists(move_file)
            assert self._storage_driver.get(self._sanitizer.concat(directory, original_file)) == content1
            assert target_storage_driver.get(self._sanitizer.concat(directory, move_file)) == content2
            assert target_storage_driver.get(move_file) == content3
            assert self._storage_driver.move(self._sanitizer.concat(directory, original_file), self._sanitizer.concat(directory, move_file), target_storage_driver)
            assert not self._storage_driver.move(self._sanitizer.concat(directory, original_file), move_file, target_storage_driver)
            assert not self._storage_driver.exists(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.exists(self._sanitizer.concat(directory, move_file))
            assert target_storage_driver.exists(move_file)
            assert not self._storage_driver.get(self._sanitizer.concat(directory, original_file))
            assert target_storage_driver.get(self._sanitizer.concat(directory, move_file)) == content1
            assert target_storage_driver.get(move_file) == content3

    @final
    @override
    def test_delete__file_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.delete("file.txt")

    @final
    @override
    def test_delete__file_is_directory__then_return_false(self) -> None:
        root: str = self._create_directory_in_storage_driver("directory1")
        directory: str = self._create_directory_in_storage_driver("directory2/directory3")

        assert self._storage_driver.exists_directory(root)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.delete(root)
        assert not self._storage_driver.delete(directory)

    @final
    @override
    def test_delete__file_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.delete("")
        assert not self._storage_driver.delete("    ")

    @final
    @override
    def test_delete__file_exists__then_return_true(self) -> None:
        assert self._storage_driver.put_file_as(self._create_byte_array(), "file.txt")
        assert self._storage_driver.put_file_as(self._create_byte_array(), self._sanitizer.sanitize("directory/file.txt"))
        assert self._storage_driver.exists("file.txt")
        assert self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))
        assert self._storage_driver.delete("file.txt")
        assert self._storage_driver.delete(self._sanitizer.sanitize("directory/file.txt"))
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))

    @final
    @override
    def test_rename__source_not_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/file.txt"))
        assert not self._storage_driver.exists("rename")
        assert not self._storage_driver.rename("file.txt", "rename")
        assert not self._storage_driver.rename(self._sanitizer.sanitize("directory/file.txt"), "rename")

    @final
    @override
    def test_rename__source_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.exists("rename")
        assert not self._storage_driver.rename("", "rename")
        assert not self._storage_driver.rename("    ", "rename")

    @final
    @override
    def test_rename__source_is_directory__then_return_false(self) -> None:
        root: str = self._create_directory_in_storage_driver("directory1")
        directory: str = self._create_directory_in_storage_driver("directory2/directory3")

        assert self._storage_driver.exists_directory(root)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.exists("file.txt")
        assert not self._storage_driver.rename(root, "file.txt")
        assert not self._storage_driver.rename(directory, "file.txt")

    @final
    @override
    def test_rename__target_exists__then_return_false(self) -> None:
        file_creator_data_to_rename: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "rename.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "rename.txt")

        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, file_creator_data_in_root.path)
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, file_creator_data_in_directory.path)

    @final
    @override
    def test_rename__target_is_root__then_return_false(self) -> None:
        file_creator_data_to_rename: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, "")
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, "    ")

    @final
    @override
    def test_rename__target_is_directory__then_return_false(self) -> None:
        file_creator_data_to_rename: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, "directory")

    @final
    @override
    def test_rename__source_exists_and_target_is_source__then_return_false(self) -> None:
        file_creator_data_to_rename: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert not self._storage_driver.rename(file_creator_data_to_rename.path, file_creator_data_to_rename.path)

    @final
    @override
    def test_rename__source_exists_and_target_not_exists__then_return_true(self) -> None:
        file_creator_data_to_rename: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")

        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert self._storage_driver.rename(file_creator_data_to_rename.path, self._sanitizer.sanitize("directory/rename.txt"))
        assert not self._storage_driver.exists(file_creator_data_to_rename.path)
        assert self._storage_driver.exists(self._sanitizer.sanitize("directory/rename.txt"))
        assert self._storage_driver.rename(self._sanitizer.sanitize("directory/rename.txt"), file_creator_data_to_rename.path)
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/rename.txt"))
        assert self._storage_driver.exists(file_creator_data_to_rename.path)
        assert not self._storage_driver.exists(self._sanitizer.sanitize("directory/rename.txt"))

    @final
    @override
    def test_files__directory_not_exists__then_return_collection_empty(self) -> None:
        assert not self._storage_driver.exists_directory("directory")
        assert len(self._storage_driver.files("directory")) == 0

    @final
    @override
    def test_files__directory_is_file__then_return_collection_empty(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert len(self._storage_driver.files(file_creator_data_in_root.path)) == 0
        assert len(self._storage_driver.files(file_creator_data_in_directory.path) )== 0

    @final
    @override
    def test_files__get__then_return_collection_string(self) -> None:
        directory_first_level = "directory1"
        directory_second_level: str = self._sanitizer.concat(directory_first_level, "directory2")

        assert self._storage_driver.make_directory(directory_first_level)
        assert self._storage_driver.make_directory(directory_second_level)
        assert self._storage_driver.exists_directory(directory_first_level)
        assert self._storage_driver.exists_directory(directory_second_level)
        assert len(self._storage_driver.files(directory_first_level)) == 0
        self._create_file_in_storage_driver(directory_first_level, "1.txt")
        assert len(self._storage_driver.files(directory_first_level)) == 1
        assert self._storage_driver.files(directory_first_level) == [self._sanitizer.concat(directory_first_level, "1.txt")]
        self._create_file_in_storage_driver(directory_first_level, "2.txt")
        assert len(self._storage_driver.files(directory_first_level)) == 2
        assert set(self._storage_driver.files(directory_first_level)) == {
            self._sanitizer.concat(directory_first_level, "1.txt"),
            self._sanitizer.concat(directory_first_level, "2.txt"),
        }
        self._create_file_in_storage_driver(directory_second_level, "1.txt")
        assert len(self._storage_driver.files(directory_first_level)) == 2
        assert set(self._storage_driver.files(directory_first_level)) == {
            self._sanitizer.concat(directory_first_level, "1.txt"),
            self._sanitizer.concat(directory_first_level, "2.txt"),
        }
        assert len(self._storage_driver.files(directory_second_level)) == 1
        assert self._storage_driver.files(directory_second_level) == [self._sanitizer.concat(directory_second_level, "1.txt")]
        assert len(self._storage_driver.files("")) == 0
        self._create_file_in_storage_driver("", "root.txt")
        assert len(self._storage_driver.files("")) == 1
        assert self._storage_driver.files("") == ["root.txt"]
        assert len(self._storage_driver.files("    ")) == 1
        assert self._storage_driver.files("    ") == ["root.txt"]

    @final
    @override
    def test_all_files__directory_not_exists__then_return_collection_empty(self) -> None:
        assert not self._storage_driver.exists_directory("directory")
        assert len(self._storage_driver.all_files("directory")) == 0

    @final
    @override
    def test_all_files__directory_is_file__then_return_collection_empty(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert len(self._storage_driver.all_files(file_creator_data_in_root.path)) == 0
        assert len(self._storage_driver.all_files(file_creator_data_in_directory.path)) == 0

    @final
    @override
    def test_all_files__get__then_return_collection_string(self) -> None:
        directory_first_level: str = "directory1"
        directory_second_level: str = self._sanitizer.concat(directory_first_level, "directory2")

        assert len(self._storage_driver.all_files("")) == 0
        assert len(self._storage_driver.all_files("    ")) == 0
        assert self._storage_driver.make_directory(directory_first_level)
        assert self._storage_driver.make_directory(directory_second_level)
        assert self._storage_driver.exists_directory(directory_first_level)
        assert self._storage_driver.exists_directory(directory_second_level)
        assert len(self._storage_driver.all_files(directory_first_level)) == 0

        self._create_file_in_storage_driver(directory_first_level, "1.txt")
        assert len(self._storage_driver.all_files(directory_first_level)) == 1
        assert set(self._storage_driver.all_files(directory_first_level)) == {self._sanitizer.concat(directory_first_level, "1.txt")}

        self._create_file_in_storage_driver(directory_first_level, "2.txt")
        assert len(self._storage_driver.all_files(directory_first_level)) == 2
        assert set(self._storage_driver.all_files(directory_first_level)) == {self._sanitizer.concat(directory_first_level, "1.txt"), self._sanitizer.concat(directory_first_level, "2.txt")}

        self._create_file_in_storage_driver(directory_second_level, "1.txt")
        assert len(self._storage_driver.all_files(directory_first_level)) == 3
        assert set(self._storage_driver.all_files(directory_first_level)) == {self._sanitizer.concat(directory_first_level, "1.txt"), self._sanitizer.concat(directory_first_level, "2.txt"), self._sanitizer.concat(directory_second_level, "1.txt")}

        assert len(self._storage_driver.all_files(directory_second_level)) == 1
        assert set(self._storage_driver.all_files(directory_second_level)) == {self._sanitizer.concat(directory_second_level, "1.txt")}

        assert len(self._storage_driver.all_files("")) == 3

        self._create_file_in_storage_driver("", "root.txt")

        assert len(self._storage_driver.all_files("")) == 4
        assert set(self._storage_driver.all_files("")) == {"root.txt", self._sanitizer.concat(directory_first_level, "1.txt"), self._sanitizer.concat(directory_first_level, "2.txt"), self._sanitizer.concat(directory_second_level, "1.txt")}

        assert len(self._storage_driver.all_files("    ")) == 4
        assert set(self._storage_driver.all_files("    ")) == {"root.txt", self._sanitizer.concat(directory_first_level, "1.txt"), self._sanitizer.concat(directory_first_level, "2.txt"), self._sanitizer.concat(directory_second_level, "1.txt")}

    @final
    @override
    def test_directories__directory_not_exists__then_return_collection_empty(self) -> None:
        assert not self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.directories("directory")

    @final
    @override
    def test_directories__directory_is_file__then_return_collection_empty(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert not self._storage_driver.directories(file_creator_data_in_root.path)
        assert not self._storage_driver.directories(file_creator_data_in_directory.path)

    @final
    @override
    def test_directories__get__then_return_collection_string(self) -> None:
        directory1: str = "directory"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_2: str = self._sanitizer.concat(directory1, "2")
        directory1_3: str = self._sanitizer.concat(directory1, "3")
        directory1_3_1: str = self._sanitizer.concat(directory1_3, "1")

        self._create_directory_in_storage_driver(directory1_1)
        assert len(self._storage_driver.directories(directory1_1)) == 0

        self._create_directory_in_storage_driver(directory1_2)
        assert len(self._storage_driver.directories(directory1_2)) == 0

        self._create_directory_in_storage_driver(directory1_3)
        assert len(self._storage_driver.directories(directory1_3)) == 0

        self._create_directory_in_storage_driver(directory1_3_1)
        assert len(self._storage_driver.directories(directory1)) == 3
        assert set(self._storage_driver.directories(directory1)) == {self._sanitizer.sanitize(directory1_1), self._sanitizer.sanitize(directory1_2), self._sanitizer.sanitize(directory1_3)}

        assert len(self._storage_driver.directories(directory1_3)) == 1
        assert set(self._storage_driver.directories(directory1_3)) == {self._sanitizer.sanitize(directory1_3_1)}

        assert len(self._storage_driver.directories("")) == 1
        assert set(self._storage_driver.directories("")) == {self._sanitizer.sanitize(directory1)}

        assert len(self._storage_driver.directories("    ")) == 1
        assert set(self._storage_driver.directories("    ")) == {self._sanitizer.sanitize(directory1)}

    @final
    @override
    def test_all_directories__directory_not_exists__then_return_collection_empty(self) -> None:
        assert not self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.all_directories("directory")

    @final
    @override
    def test_all_directories__directory_is_file__then_return_collection_empty(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)

        assert not self._storage_driver.all_directories(file_creator_data_in_root.path)
        assert not self._storage_driver.all_directories(file_creator_data_in_directory.path)

    @final
    @override
    def test_all_directories__get__then_return_collection_string(self) -> None:
        directory1: str = "directory"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_2: str = self._sanitizer.concat(directory1, "2")
        directory1_3: str = self._sanitizer.concat(directory1, "3")
        directory1_3_1: str = self._sanitizer.concat(directory1_3, "1")

        assert len(self._storage_driver.all_directories("")) == 0
        assert len(self._storage_driver.all_directories("    ")) == 0

        self._create_directory_in_storage_driver(directory1_1)
        assert len(self._storage_driver.all_directories(directory1_1)) == 0

        self._create_directory_in_storage_driver(directory1_2)
        assert len(self._storage_driver.all_directories(directory1_2)) == 0

        self._create_directory_in_storage_driver(directory1_3)
        assert len(self._storage_driver.all_directories(directory1_3)) == 0

        self._create_directory_in_storage_driver(directory1_3_1)
        assert len(self._storage_driver.all_directories(directory1)) == 4
        assert set(self._storage_driver.all_directories(directory1)) == {self._sanitizer.sanitize(directory1_1), self._sanitizer.sanitize(directory1_2), self._sanitizer.sanitize(directory1_3), self._sanitizer.sanitize(directory1_3_1)}

        assert len(self._storage_driver.all_directories(directory1_3)) == 1
        assert set(self._storage_driver.all_directories(directory1_3)) == {self._sanitizer.sanitize(directory1_3_1)}

        assert len(self._storage_driver.all_directories("")) == 5
        assert set(self._storage_driver.all_directories("")) == {self._sanitizer.sanitize(directory1), self._sanitizer.sanitize(directory1_1), self._sanitizer.sanitize(directory1_2), self._sanitizer.sanitize(directory1_3), self._sanitizer.sanitize(directory1_3_1)}

        assert len(self._storage_driver.all_directories("    ")) == 5
        assert set(self._storage_driver.all_directories("    ")) == {self._sanitizer.sanitize(directory1), self._sanitizer.sanitize(directory1_1), self._sanitizer.sanitize(directory1_2), self._sanitizer.sanitize(directory1_3), self._sanitizer.sanitize(directory1_3_1)}

    @final
    @override
    def test_exists_directory__directory_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists("directory")
        assert not self._storage_driver.exists_directory("directory")

    @final
    @override
    def test_exists_directory__directory_is_file__then_return_false(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert not self._storage_driver.exists_directory(file_creator_data_in_root.path)
        assert not self._storage_driver.exists_directory(file_creator_data_in_directory.path)

    @final
    @override
    def test_exists_directory__directory_is_root__then_return_true(self) -> None:
        assert self._storage_driver.exists_directory("")
        assert self._storage_driver.exists_directory("    ")

    @final
    @override
    def test_exists_directory__directory_in_directory__then_return_true(self) -> None:
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))

    @final
    @override
    def test_exists_directory__directory_in_root__then_return_true(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")

    @final
    @override
    def test_copy_directory__source_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("directory1")
        assert not self._storage_driver.exists_directory("directory2")
        assert not self._storage_driver.copy_directory("directory1", "directory2")
        assert not self._storage_driver.copy_directory("directory1", "")

    @final
    @override
    def test_copy_directory__source_is_file__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory1", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory2")

        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.copy_directory(file_creator_data.path, directory)
        assert not self._storage_driver.copy_directory(file_creator_data.path, "")

    @final
    @override
    def test_copy_directory__source_is_root__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.copy_directory("", "directory")
        assert not self._storage_driver.copy_directory("    ", "directory")

    @final
    @override
    def test_copy_directory__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
        assert not self._storage_driver.copy_directory("directory", "")
        assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/1"), "directory")
        assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/1/2"), self._sanitizer.sanitize("directory/1"))

    @final
    @override
    def test_copy_directory__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
        assert not self._storage_driver.copy_directory("directory", "directory")
        assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/1"))
        assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/2/1"))
        assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/2/1/1"))
        assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2"))
        assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1"))
        assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1/1"))

    @final
    @override
    def test_copy_directory__target_is_file__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory")

        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.copy_directory(directory, file_creator_data.path)

    @final
    @override
    def test_copy_directory__target_not_exists__then_return_false(self) -> None:
        directory1: str = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2: str = "directory2"
        file1: str = "file1.txt"
        file2: str = "file2.txt"
        file3: str = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()

        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

        assert not self._storage_driver.exists_directory(directory2)
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 0
        assert len(self._storage_driver.directories(directory2)) == 0
        assert len(self._storage_driver.all_directories(directory2)) == 0
        assert not self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert not self._storage_driver.copy_directory(directory1_1, directory2)
        assert not self._storage_driver.exists_directory(directory2)
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 0
        assert len(self._storage_driver.directories(directory2)) == 0
        assert len(self._storage_driver.all_directories(directory2)) == 0
        assert not self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))

    @final
    @override
    def test_copy_directory__target_is_root__then_return_true(self) -> None:
        directory1: str = "directory"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        file1: str = "file1.txt"
        file2: str = "file2.txt"
        file3: str = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()

        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

        assert len(self._storage_driver.files(directory1_1)) == 0
        assert len(self._storage_driver.all_files(directory1_1)) == 2
        assert len(self._storage_driver.directories(directory1_1)) == 2
        assert len(self._storage_driver.all_directories(directory1_1)) == 2
        assert len(self._storage_driver.files("")) == 1
        assert len(self._storage_driver.all_files("")) == 3
        assert len(self._storage_driver.directories("")) == 1
        assert len(self._storage_driver.all_directories("")) == 4
        assert not self._storage_driver.exists_directory("1")
        assert self._storage_driver.copy_directory(directory1_1, "")
        assert len(self._storage_driver.files(directory1_1)) == 0
        assert len(self._storage_driver.all_files(directory1_1)) == 2
        assert len(self._storage_driver.directories(directory1_1)) == 2
        assert len(self._storage_driver.all_directories(directory1_1)) == 2
        assert len(self._storage_driver.files("")) == 1
        assert len(self._storage_driver.all_files("")) == 5
        assert len(self._storage_driver.directories("")) == 2
        assert len(self._storage_driver.all_directories("")) == 7
        assert set(self._storage_driver.all_files("")) == set([
            self._sanitizer.concat(directory1_1_1, file1),
            self._sanitizer.concat(directory1_1_2, file2),
            self._sanitizer.concat(file3),
            self._sanitizer.concat("1", "1", file1),
            self._sanitizer.concat("1", "2", file2)
        ])
        assert self._storage_driver.exists_directory("1")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("1/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("1/2"))

    @final
    @override
    def test_copy_directory__target_is_empty_directory__then_return_true(self) -> None:
        directory1: str = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2: str = "directory2"
        file1: str = "file1.txt"
        file2: str = "file2.txt"
        file3: str = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()

        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

        assert self._storage_driver.make_directory(directory2)
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 0
        assert len(self._storage_driver.directories(directory2)) == 0
        assert len(self._storage_driver.all_directories(directory2)) == 0
        assert not self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.copy_directory(directory1_1, directory2)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 2
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 3
        assert set(self._storage_driver.all_files(directory2)) == {self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)}
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))

    @final
    @override
    def test_copy_directory__target_is_non_empty_directory__then_return_true(self) -> None:
        directory1: str = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2: str = "directory2"
        directory2_1: str = self._sanitizer.concat(directory2, "1")
        directory2_1_1: str = self._sanitizer.concat(directory2_1, "1")
        file1: str = "file1.txt"
        file2: str = "file2.txt"
        file3: str = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()

        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), self._sanitizer.concat(directory2_1_1, file1))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 1
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 2
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content3.encode("UTF-8")
        assert self._storage_driver.copy_directory(directory1_1, directory2)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 2
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 3
        assert set(self._storage_driver.all_files(directory2)) == {self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)}
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))

    @final
    @override
    def test_copy_directory__another_storage_driver__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            assert self._storage_driver.make_directory("directory")
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
            assert self._storage_driver.exists_directory("directory")
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
            assert target_storage_driver.make_directory("directory")
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
            assert target_storage_driver.exists_directory("directory")
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
            assert not self._storage_driver.copy_directory("directory", "", target_storage_driver)
            assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/1"), "directory", target_storage_driver)
            assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/1/2"), self._sanitizer.sanitize("directory/1"), target_storage_driver)

    @final
    @override
    def test_copy_directory__another_storage_driver__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            assert self._storage_driver.make_directory("directory")
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert target_storage_driver.make_directory("directory")
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert not self._storage_driver.copy_directory("directory", "directory", target_storage_driver)
            assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/1"), target_storage_driver)
            assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/2/1"), target_storage_driver)
            assert not self._storage_driver.copy_directory("directory", self._sanitizer.sanitize("directory/2/1/1"), target_storage_driver)
            assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2"), target_storage_driver)
            assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1"), target_storage_driver)
            assert not self._storage_driver.copy_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1/1"), target_storage_driver)

    @final
    @override
    def test_copy_directory__another_storage_driver__target_is_file__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt", target_storage_driver)
            directory: str = self._create_directory_in_storage_driver("directory")

            assert target_storage_driver.exists(file_creator_data.path)
            assert self._storage_driver.exists_directory(directory)
            assert not self._storage_driver.copy_directory(directory, file_creator_data.path, target_storage_driver)

    @final
    @override
    def test_copy_directory__another_storage_driver__target_not_exists__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1: str = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2: str = "directory2"
            file1: str = "file1.txt"
            file2: str = "file2.txt"
            file3: str = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert not target_storage_driver.exists_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert not self._storage_driver.copy_directory(directory1_1, directory2, target_storage_driver)
            assert not target_storage_driver.exists_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))

    @final
    @override
    def test_copy_directory__another_storage_driver__target_is_root__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1: str = "directory"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            file1: str = "file1.txt"
            file2: str = "file2.txt"
            file3: str = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert len(self._storage_driver.files(directory1_1)) == 0
            assert len(self._storage_driver.all_files(directory1_1)) == 2
            assert len(self._storage_driver.directories(directory1_1)) == 2
            assert len(self._storage_driver.all_directories(directory1_1)) == 2
            assert len(target_storage_driver.files("")) == 0
            assert len(target_storage_driver.all_files("")) == 0
            assert len(target_storage_driver.directories("")) == 0
            assert len(target_storage_driver.all_directories("")) == 0
            assert not target_storage_driver.exists_directory("1")

            assert set(self._storage_driver.all_files("")) == set([
                self._sanitizer.concat(directory1_1_1, file1),
                self._sanitizer.concat(directory1_1_2, file2),
                file3
            ])

            assert self._storage_driver.copy_directory(directory1_1, "", target_storage_driver)
            assert len(self._storage_driver.files(directory1_1)) == 0
            assert len(self._storage_driver.all_files(directory1_1)) == 2
            assert len(self._storage_driver.directories(directory1_1)) == 2
            assert len(self._storage_driver.all_directories(directory1_1)) == 2
            assert len(target_storage_driver.files("")) == 0
            assert len(target_storage_driver.all_files("")) == 2
            assert len(target_storage_driver.directories("")) == 1
            assert len(target_storage_driver.all_directories("")) == 3
            assert set(target_storage_driver.all_files("")) == set([
                self._sanitizer.concat("1", "1", file1),
                self._sanitizer.concat("1", "2", file2)
            ])

            assert target_storage_driver.exists_directory("1")
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("1/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("1/2"))

    @final
    @override
    def test_copy_directory__another_storage_driver__target_is_empty_directory__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1: str = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2: str = "directory2"
            file1: str = "file1.txt"
            file2: str = "file2.txt"
            file3: str = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert target_storage_driver.make_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert self._storage_driver.copy_directory(directory1_1, directory2, target_storage_driver)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert set(self._storage_driver.all_files("")) == {self._sanitizer.concat(directory1_1_1, file1), self._sanitizer.concat(directory1_1_2, file2), file3}
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 2
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 3
            assert set(target_storage_driver.all_files("")) == {self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)}
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))

    @final
    @override
    def test_copy_directory__another_storage_driver__target_is_non_empty_directory__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1: str = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2: str = "directory2"
            directory2_1: str = self._sanitizer.concat(directory2, "1")
            directory2_1_1: str = self._sanitizer.concat(directory2_1, "1")
            file1: str = "file1.txt"
            file2: str = "file2.txt"
            file3: str = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            target_storage_driver.put_file_as(content3.encode("UTF-8"), self._sanitizer.concat(directory2_1_1, file1))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert set(self._storage_driver.all_files("")) == {self._sanitizer.concat(directory1_1_1, file1), self._sanitizer.concat(directory1_1_2, file2), file3}
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 1
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 2
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content3.encode("UTF-8")
            assert self._storage_driver.copy_directory(directory1_1, directory2, target_storage_driver)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 2
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 3
            assert set(target_storage_driver.all_files("")) == {self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)}
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))
            assert target_storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content1.encode("UTF-8")

    @final
    @override
    def test_move_directory__source_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("directory1")
        assert not self._storage_driver.exists_directory("directory2")
        assert not self._storage_driver.move_directory("directory1", "directory2")
        assert not self._storage_driver.move_directory("directory1", "")

    @final
    @override
    def test_move_directory__source_is_file__then_return_false(self) -> None:
        file_creator_data: 'FileCreatorData' = self._create_file_in_storage_driver("directory1", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory2")

        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.move_directory(file_creator_data.path, directory)
        assert not self._storage_driver.move_directory(file_creator_data.path, "")

    @final
    @override
    def test_move_directory__source_is_root__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.move_directory("", "directory")
        assert not self._storage_driver.move_directory("    ", "directory")

    @final
    @override
    def test_move_directory__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
        assert not self._storage_driver.move_directory("directory", "")
        assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/1"), "directory")
        assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/1/2"), self._sanitizer.sanitize("directory/1"))

    @final
    @override
    def test_move_directory__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
        assert not self._storage_driver.move_directory("directory", "directory")
        assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/1"))
        assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/2/1"))
        assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/2/1/1"))
        assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2"))
        assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1"))
        assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1/1"))

    @final
    @override
    def test_move_directory__target_is_file__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        directory: str = self._create_directory_in_storage_driver("directory")
        assert self._storage_driver.exists(file_creator_data.path)
        assert self._storage_driver.exists_directory(directory)
        assert not self._storage_driver.move_directory(directory, file_creator_data.path)

    @final
    @override
    def test_move_directory__target_not_exists__then_return_false(self) -> None:
        directory1 = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2 = "directory2"
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()
        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)
        assert not self._storage_driver.exists_directory(directory2)
        assert not self._storage_driver.move_directory(directory1_1, directory2)
        assert not self._storage_driver.exists_directory(directory2)

    @final
    @override
    def test_move_directory__target_is_root__then_return_true(self) -> None:
        directory1 = "directory"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()
        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)
        assert len(self._storage_driver.files(directory1_1)) == 0
        assert len(self._storage_driver.all_files(directory1_1)) == 2
        assert len(self._storage_driver.directories(directory1_1)) == 2
        assert len(self._storage_driver.all_directories(directory1_1)) == 2
        assert len(self._storage_driver.files("")) == 1
        assert len(self._storage_driver.all_files("")) == 3
        assert len(self._storage_driver.directories("")) == 1
        assert len(self._storage_driver.all_directories("")) == 4
        assert not self._storage_driver.exists_directory("1")
        assert self._storage_driver.move_directory(directory1_1, "")
        assert len(self._storage_driver.files(directory1_1)) == 0
        assert len(self._storage_driver.all_files(directory1_1)) == 0
        assert len(self._storage_driver.directories(directory1_1)) == 0
        assert len(self._storage_driver.all_directories(directory1_1)) == 0
        assert len(self._storage_driver.files("")) == 1
        assert len(self._storage_driver.all_files("")) == 3
        assert len(self._storage_driver.directories(""))== 2
        assert len(self._storage_driver.all_directories("")) == 4
        assert set(self._storage_driver.all_files("")) == set([self._sanitizer.concat("1", "1", file1), self._sanitizer.concat("1", "2", file2), self._sanitizer.concat(file3)])
        assert self._storage_driver.exists_directory("1")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("1/1"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("1/2"))

    @final
    @override
    def test_move_directory__target_is_empty_directory__then_return_true(self) -> None:
        directory1 = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2 = "directory2"
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()
        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)
        assert self._storage_driver.make_directory(directory2)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 0
        assert len(self._storage_driver.directories(directory2)) == 0
        assert len(self._storage_driver.all_directories(directory2)) == 0
        assert not self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.move_directory(directory1_1, directory2)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 0
        assert len(self._storage_driver.directories(directory1)) == 0
        assert len(self._storage_driver.all_directories(directory1)) == 0
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 2
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 3
        assert set(self._storage_driver.all_files(directory2)) == set([self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)])
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))

    @final
    @override
    def test_move_directory__target_is_non_empty_directory__then_return_true(self) -> None:
        directory1 = "directory1"
        directory1_1: str = self._sanitizer.concat(directory1, "1")
        directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
        directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
        directory2 = "directory2"
        directory2_1: str = self._sanitizer.concat(directory2, "1")
        directory2_1_1: str = self._sanitizer.concat(directory2_1, "1")
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content1: str = self._create_string()
        content2: str = self._create_string()
        content3: str = self._create_string()
        self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
        self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), self._sanitizer.concat(directory2_1_1, file1))
        self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 2
        assert len(self._storage_driver.directories(directory1)) == 1
        assert len(self._storage_driver.all_directories(directory1)) == 3
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 1
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 2
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content3.encode("UTF-8")
        assert self._storage_driver.move_directory(directory1_1, directory2)
        assert len(self._storage_driver.files(directory1)) == 0
        assert len(self._storage_driver.all_files(directory1)) == 0
        assert len(self._storage_driver.directories(directory1)) == 0
        assert len(self._storage_driver.all_directories(directory1)) == 0
        assert len(self._storage_driver.files(directory2)) == 0
        assert len(self._storage_driver.all_files(directory2)) == 2
        assert len(self._storage_driver.directories(directory2)) == 1
        assert len(self._storage_driver.all_directories(directory2)) == 3
        assert set(self._storage_driver.all_files(directory2)) == set([self._sanitizer.concat(directory2, "1", "1", file1), self._sanitizer.concat(directory2, "1", "2", file2)])
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
        assert self._storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))
        assert self._storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content1.encode("UTF-8")

    @final
    @override
    def test_move_directory__another_storage_driver__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            assert self._storage_driver.make_directory("directory")
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
            assert self._storage_driver.exists_directory("directory")
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
            assert target_storage_driver.make_directory("directory")
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1/2"))
            assert target_storage_driver.exists_directory("directory")
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1/2"))
            assert not self._storage_driver.move_directory("directory", "", target_storage_driver)
            assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/1"), "directory", target_storage_driver)
            assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/1/2"), self._sanitizer.sanitize("directory/1"), target_storage_driver)

    @final
    @override
    def test_move_directory__another_storage_driver__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            assert self._storage_driver.make_directory("directory")
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
            assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert target_storage_driver.make_directory("directory")
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1"))
            assert target_storage_driver.make_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("directory/2/1/1"))
            assert not self._storage_driver.move_directory("directory", "directory", target_storage_driver)
            assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/1"), target_storage_driver)
            assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/2/1"), target_storage_driver)
            assert not self._storage_driver.move_directory("directory", self._sanitizer.sanitize("directory/2/1/1")), target_storage_driver
            assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2"), target_storage_driver)
            assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1"), target_storage_driver)
            assert not self._storage_driver.move_directory(self._sanitizer.sanitize("directory/2"), self._sanitizer.sanitize("directory/2/1/1"), target_storage_driver)

    @final
    @override
    def test_move_directory__another_storage_driver__target_is_file__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            file_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "file.txt", target_storage_driver)
            directory = self._create_directory_in_storage_driver("directory")
            assert target_storage_driver.exists(file_creator_data.path)
            assert self._storage_driver.exists_directory(directory)
            assert not self._storage_driver.move_directory(directory, file_creator_data.path, target_storage_driver)

    @final
    @override
    def test_move_directory__another_storage_driver__target_not_exists__then_return_false(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1 = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2 = "directory2"
            file1 = "file1.txt"
            file2 = "file2.txt"
            file3 = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert not target_storage_driver.exists_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert not self._storage_driver.move_directory(directory1_1, directory2, target_storage_driver)
            assert not target_storage_driver.exists_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))

    @final
    @override
    def test_move_directory__another_storage_driver__target_is_root__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1 = "directory"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            file1 = "file1.txt"
            file2 = "file2.txt"
            file3 = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert len(self._storage_driver.files(directory1_1)) == 0
            assert len(self._storage_driver.all_files(directory1_1)) == 2
            assert len(self._storage_driver.directories(directory1_1)) == 2
            assert len(self._storage_driver.all_directories(directory1_1)) == 2
            assert len(target_storage_driver.files("")) == 0
            assert len(target_storage_driver.all_files("")) == 0
            assert len(target_storage_driver.directories("")) == 0
            assert len(target_storage_driver.all_directories("")) == 0
            assert not target_storage_driver.exists_directory("1")
            assert self._storage_driver.move_directory(directory1_1, "", target_storage_driver)
            assert len(self._storage_driver.files(directory1_1)) == 0
            assert len(self._storage_driver.all_files(directory1_1)) == 0
            assert len(self._storage_driver.directories(directory1_1)) == 0
            assert len(self._storage_driver.all_directories(directory1_1)) == 0
            assert len(target_storage_driver.files("")) == 0
            assert len(target_storage_driver.all_files("")) == 2
            assert len(target_storage_driver.directories("")) == 1
            assert len(target_storage_driver.all_directories("")) == 3
            assert target_storage_driver.exists_directory("1")
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("1/1"))
            assert target_storage_driver.exists_directory(self._sanitizer.sanitize("1/2"))

    @final
    @override
    def test_move_directory__another_storage_driver__target_is_empty_directory__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1 = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2 = "directory2"
            file1 = "file1.txt"
            file2 = "file2.txt"
            file3 = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)
            assert target_storage_driver.make_directory(directory2)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 0
            assert len(target_storage_driver.directories(directory2)) == 0
            assert len(target_storage_driver.all_directories(directory2)) == 0
            assert not target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert self._storage_driver.move_directory(directory1_1, directory2, target_storage_driver)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 0
            assert len(self._storage_driver.directories(directory1)) == 0
            assert len(self._storage_driver.all_directories(directory1)) == 0
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 2
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 3
            assert set(target_storage_driver.all_files("")) == set([
                self._sanitizer.concat(directory2, "1", "1", file1),
                self._sanitizer.concat(directory2, "1", "2", file2)
            ])
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))

    @final
    @override
    def test_move_directory__another_storage_driver__target_is_non_empty_directory__then_return_true(self) -> None:
        with self._create_storage_driver_secondary() as target_storage_driver:
            directory1 = "directory1"
            directory1_1: str = self._sanitizer.concat(directory1, "1")
            directory1_1_1: str = self._sanitizer.concat(directory1_1, "1")
            directory1_1_2: str = self._sanitizer.concat(directory1_1, "2")
            directory2 = "directory2"
            directory2_1: str = self._sanitizer.concat(directory2, "1")
            directory2_1_1: str = self._sanitizer.concat(directory2_1, "1")
            file1 = "file1.txt"
            file2 = "file2.txt"
            file3 = "file3.txt"
            content1: str = self._create_string()
            content2: str = self._create_string()
            content3: str = self._create_string()

            self._storage_driver.put_file_as(content1.encode("UTF-8"), self._sanitizer.concat(directory1_1_1, file1))
            self._storage_driver.put_file_as(content2.encode("UTF-8"), self._sanitizer.concat(directory1_1_2, file2))
            target_storage_driver.put_file_as(content3.encode("UTF-8"), self._sanitizer.concat(directory2_1_1, file1))
            self._storage_driver.put_file_as(content3.encode("UTF-8"), file3)

            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 2
            assert len(self._storage_driver.directories(directory1)) == 1
            assert len(self._storage_driver.all_directories(directory1)) == 3
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 1
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 2
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content3.encode("UTF-8")
            assert self._storage_driver.move_directory(directory1_1, directory2, target_storage_driver)
            assert len(self._storage_driver.files(directory1)) == 0
            assert len(self._storage_driver.all_files(directory1)) == 0
            assert len(self._storage_driver.directories(directory1)) == 0
            assert len(self._storage_driver.all_directories(directory1)) == 0
            assert len(target_storage_driver.files(directory2)) == 0
            assert len(target_storage_driver.all_files(directory2)) == 2
            assert len(target_storage_driver.directories(directory2)) == 1
            assert len(target_storage_driver.all_directories(directory2)) == 3
            assert set(target_storage_driver.all_files("")) == set([
                self._sanitizer.concat(directory2, "1", "1", file1),
                self._sanitizer.concat(directory2, "1", "2", file2)
            ])
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "1"))
            assert target_storage_driver.exists_directory(self._sanitizer.concat(directory2, "1", "2"))
            assert target_storage_driver.get(self._sanitizer.concat(directory2_1_1, file1)) == content1.encode("UTF-8")

    @final
    @override
    def test_make_directory__directory_not_exists__then_return_true(self) -> None:
        assert not self._storage_driver.exists_directory("directory1")
        assert not self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert not self._storage_driver.exists_directory("directory3")
        assert not self._storage_driver.exists_directory(self._sanitizer.sanitize("directory3/directory4"))
        assert self._storage_driver.make_directory("directory1")
        assert self._storage_driver.exists_directory("directory1")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory3/directory4"))
        assert self._storage_driver.exists_directory("directory3")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory3/directory4"))

    @final
    @override
    def test_make_directory__directory_already_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("directory1")
        assert not self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert not self._storage_driver.exists_directory("directory3")
        assert not self._storage_driver.exists_directory(self._sanitizer.sanitize("directory3/directory4"))
        assert self._storage_driver.make_directory("directory1")
        assert self._storage_driver.exists_directory("directory1")
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.make_directory(self._sanitizer.sanitize("directory3/directory4"))
        assert self._storage_driver.exists_directory("directory3")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory3/directory4"))
        assert not self._storage_driver.make_directory("directory1")
        assert not self._storage_driver.make_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert not self._storage_driver.make_directory(self._sanitizer.sanitize("directory3/directory4"))

    @final
    @override
    def test_make_directory__directory_is_file__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")
        assert self._storage_driver.exists(file_creator_data.path)
        assert not self._storage_driver.exists_directory(file_creator_data.path)
        assert not self._storage_driver.make_directory(file_creator_data.path)

    @final
    @override
    def test_make_directory__directory_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.make_directory("")
        assert not self._storage_driver.make_directory("    ")

    @final
    @override
    def test_delete_directory__directory_not_exists__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.delete_directory("directory")

    @final
    @override
    def test_delete_directory__directory_is_file__then_return_false(self) -> None:
        file_creator_data_in_root: FileCreatorData = self._create_file_in_storage_driver("", "file.txt")
        file_creator_data_in_directory: FileCreatorData = self._create_file_in_storage_driver("directory", "file.txt")
        assert self._storage_driver.exists(file_creator_data_in_root.path)
        assert self._storage_driver.exists(file_creator_data_in_directory.path)
        assert not self._storage_driver.delete_directory(file_creator_data_in_root.path)
        assert not self._storage_driver.delete_directory(file_creator_data_in_directory.path)

    @final
    @override
    def test_delete_directory__directory_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.delete_directory("")
        assert not self._storage_driver.delete_directory("    ")

    @final
    @override
    def test_delete_directory__directory_is_empty__then_return_true(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert self._storage_driver.delete_directory("directory")
        assert not self._storage_driver.exists_directory("directory")

    @final
    @override
    def test_delete_directory__directory_has_file__then_return_true(self) -> None:
        file_creator_data1: FileCreatorData = self._create_file_in_storage_driver("directory", "file1.txt")
        file_creator_data2: FileCreatorData = self._create_file_in_storage_driver("directory", "file2.txt")

        assert self._storage_driver.exists(file_creator_data1.path)
        assert self._storage_driver.exists(file_creator_data2.path)
        assert self._storage_driver.exists_directory("directory")
        assert len(self._storage_driver.files("directory")) == 2

        assert self._storage_driver.delete_directory("directory")
        assert not self._storage_driver.exists_directory("directory")
        assert len(self._storage_driver.files("directory")) == 0

    @final
    @override
    def test_delete_directory__directory_has_directories_and_files__then_return_true(self) -> None:
        file_creator_data1: FileCreatorData = self._create_file_in_storage_driver("directory1", "file1.txt")
        file_creator_data2: FileCreatorData = self._create_file_in_storage_driver("directory1", "file2.txt")
        file_creator_data3: FileCreatorData = self._create_file_in_storage_driver("directory1/directory2", "file3.txt")
        file_creator_data4: FileCreatorData = self._create_file_in_storage_driver("directory1/directory3", "file4.txt")

        assert self._storage_driver.exists(file_creator_data1.path)
        assert self._storage_driver.exists(file_creator_data2.path)
        assert self._storage_driver.exists(file_creator_data3.path)
        assert self._storage_driver.exists(file_creator_data4.path)
        assert self._storage_driver.exists_directory("directory1")
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory2"))
        assert self._storage_driver.exists_directory(self._sanitizer.sanitize("directory1/directory3"))
        assert len(self._storage_driver.files("directory1")) == 2
        assert len(self._storage_driver.all_files("directory1")) == 4

        assert self._storage_driver.delete_directory("directory1")
        assert not self._storage_driver.exists_directory("directory1")
        assert len(self._storage_driver.files("directory1")) == 0
        assert len(self._storage_driver.all_files("directory1")) == 0

    @final
    @override
    def test_rename_directory__source_not_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("root")
        assert self._storage_driver.exists_directory("root")
        assert not self._storage_driver.exists_directory("no-exists")
        assert not self._storage_driver.exists_directory(self._sanitizer.sanitize("root/no-exists"))
        assert not self._storage_driver.exists_directory("rename")
        assert not self._storage_driver.exists("no-exists")
        assert not self._storage_driver.exists(self._sanitizer.sanitize("root/no-exists"))
        assert not self._storage_driver.exists("rename")

        assert not self._storage_driver.rename_directory("no-exists", "rename")
        assert not self._storage_driver.rename_directory(self._sanitizer.sanitize("root/no-exists"), "rename")

    @final
    @override
    def test_rename_directory__source_is_root__then_return_false(self) -> None:
        assert not self._storage_driver.exists_directory("rename")
        assert not self._storage_driver.rename_directory("", "rename")
        assert not self._storage_driver.rename_directory("    ", "rename")

    @final
    @override
    def test_rename_directory__source_is_file__then_return_false(self) -> None:
        root_creator_data: FileCreatorData = self._create_file_in_storage_driver("", "root.txt")
        directory_creator_data: FileCreatorData = self._create_file_in_storage_driver("directory", "directory.txt")

        assert self._storage_driver.exists(root_creator_data.path)
        assert self._storage_driver.exists(directory_creator_data.path)
        assert not self._storage_driver.exists_directory(root_creator_data.path)
        assert not self._storage_driver.exists_directory(directory_creator_data.path)
        assert not self._storage_driver.exists_directory("rename")
        assert not self._storage_driver.rename_directory(root_creator_data.path, "rename")
        assert not self._storage_driver.rename_directory(directory_creator_data.path, "rename")

    @final
    @override
    def test_rename_directory__target_exists__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory1")
        assert self._storage_driver.make_directory("directory2")
        assert self._storage_driver.exists_directory("directory1")
        assert self._storage_driver.exists_directory("directory2")
        assert not self._storage_driver.rename_directory("directory1", "directory2")

    @final
    @override
    def test_rename_directory__target_is_root__then_return_false(self) -> None:
        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.rename_directory("directory", "")
        assert not self._storage_driver.rename_directory("directory", "    ")

    @final
    @override
    def test_rename_directory__target_is_file__then_return_false(self) -> None:
        file_creator_data: FileCreatorData = self._create_file_in_storage_driver("rename", "file.txt")

        assert self._storage_driver.make_directory("directory")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.rename_directory("directory", file_creator_data.path)

    @final
    @override
    def test_rename_directory__source_exists_and_target_not_exists__then_return_true(self) -> None:
        self._create_file_in_storage_driver("directory", "file.txt")

        assert self._storage_driver.make_directory("root")
        assert self._storage_driver.exists_directory("root")
        assert self._storage_driver.exists_directory("directory")
        assert not self._storage_driver.exists_directory("rename1")
        assert not self._storage_driver.exists_directory("rename2")
        assert len(self._storage_driver.files("root")) == 0
        assert len(self._storage_driver.files("directory")) == 1

        assert self._storage_driver.rename_directory("root", "rename1")
        assert self._storage_driver.rename_directory("directory", "rename2")
        assert not self._storage_driver.exists_directory("root")
        assert not self._storage_driver.exists_directory("directory")
        assert self._storage_driver.exists_directory("rename1")
        assert self._storage_driver.exists_directory("rename2")
        assert len(self._storage_driver.directories("")) == 2
        assert len(self._storage_driver.files("rename1")) == 0
        assert len(self._storage_driver.files("rename2")) == 1

    @final
    @override
    def test_get_metadata__source_not_exists__then_return_optional_none(self) -> None:
        assert self._storage_driver.get_metadata("file.txt") is None
        assert self._storage_driver.get_metadata("directory") is None

    @final
    @override
    def test_get_metadata__from_file__then_return_optional_metadata(self) -> None:
        directory = "directory"
        file = "file.txt"
        content: str = self._create_string(1000)
        self._storage_driver.put_file_as(content.encode("UTF-8"), self._sanitizer.concat(directory, file))
        metadata: Optional[Metadata] = self._storage_driver.get_metadata(self._sanitizer.concat(directory, file))

        assert metadata
        assert metadata.creation_time > 0
        assert metadata.last_access_time > 0
        assert metadata.last_modified > 0
        assert metadata.media_type == "text/plain"
        assert metadata.size.length == len(content.encode("UTF-8"))
        assert metadata.size.human_readable == humanize.naturalsize(len(content.encode("UTF-8")))
        assert not metadata.is_directory
        assert metadata.is_file
        assert not metadata.is_symbolic_link

    @final
    @override
    def test_get_metadata__from_folder__then_return_optional_metadata(self) -> None:
        directory = "directory"
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content: str = self._create_string(1000)

        assert self._storage_driver.put_file_as(content.encode("UTF-8"), self._sanitizer.concat(directory, file1))
        assert self._storage_driver.put_file_as(content.encode("UTF-8"), self._sanitizer.concat(directory, file2))
        assert self._storage_driver.put_file_as(content.encode("UTF-8"), file3)
        metadata: Optional[Metadata] = self._storage_driver.get_metadata(directory)

        assert metadata
        assert metadata.creation_time > 0
        assert metadata.last_access_time > 0
        assert metadata.last_modified > 0
        assert metadata.media_type == ""
        assert metadata.size.length == len(content.encode("UTF-8")) * 2
        assert metadata.size.human_readable == humanize.naturalsize(len(content.encode("UTF-8")) * 2)
        assert metadata.is_directory
        assert not metadata.is_file
        assert not metadata.is_symbolic_link

    @final
    @override
    def test_get_metadata__from_root__then_return_optional_metadata(self) -> None:
        root: str = self._storage_driver.get_root()
        directory = "directory"
        file1 = "file1.txt"
        file2 = "file2.txt"
        file3 = "file3.txt"
        content: str = self._create_string(1000)

        assert self._storage_driver.put_file_as(content.encode("UTF-8"), self._sanitizer.concat(directory, file1))
        assert self._storage_driver.put_file_as(content.encode("UTF-8"), self._sanitizer.concat(directory, file2))
        assert self._storage_driver.put_file_as(content.encode("UTF-8"), file3)
        metadata: Optional[Metadata] = self._storage_driver.get_metadata("")

        assert metadata
        assert metadata.creation_time > 0
        assert metadata.last_access_time > 0
        assert metadata.last_modified > 0
        assert metadata.media_type == ""
        assert metadata.size.length == len(content.encode("UTF-8")) * 3
        assert metadata.size.human_readable == humanize.naturalsize(len(content.encode("UTF-8")) * 3)
        assert metadata.is_directory
        assert not metadata.is_file
        assert not metadata.is_symbolic_link
        # ensure that the root is the original
        assert self._sanitizer.sanitize(self._storage_driver.get_root()) == self._sanitizer.sanitize(root)
