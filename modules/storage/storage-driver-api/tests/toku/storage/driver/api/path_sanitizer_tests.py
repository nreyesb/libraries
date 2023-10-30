# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=attribute-defined-outside-init
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: path_sanitizer_tests.py
Author: Toku Dev
"""
import pytest
from toku.storage.driver.api import PathSanitizer
from toku.storage.driver.api import DirectorySeparator


class PathSanitizerTests:
    """
    Provides test cases for PathSanitizer class.
    """

    FILE_NAME_TO_TEST: str = "1.txt"

    @pytest.fixture(params=[
        (DirectorySeparator.SLASH, DirectorySeparator.SLASH),
        (DirectorySeparator.SLASH, DirectorySeparator.BACKSLASH),
        (DirectorySeparator.BACKSLASH, DirectorySeparator.SLASH),
        (DirectorySeparator.BACKSLASH, DirectorySeparator.BACKSLASH),
    ], autouse=True)
    def setup_test(self, request: pytest.FixtureRequest) -> None:
        """
        Creates the instance of the PathSanitizer using the `separator_sanitized`.

        The `request` provides a param with the list of tuples to test all the possible combinations of directory
        separators, that way it's possible ensure that all combinations work as expected, it considers:

        1) expected separator -> /  with orignal separator -> /
        2) expected separator -> /  with orignal separator -> \\
        3) expected separator -> \\ with orignal separator -> /
        4) expected separator -> \\ with orignal separator -> \\

        First position is always the final separator expected after sanitizing the path and the
        second position is always the original separator reported into the path, for example:

        - In the case 2 the original path is:

            \\root\\folder\\file.text

          and the final path must be:

            /root/folder/file.text

        - In the case 3 the original path is:

            /root/folder/file.text

          and the final path must be:

            \\root\\folder\\file.text

        Args:
            request (FixtureRequest): The tuple with the expected and original directory separators
        """
        self.separator_sanitized: DirectorySeparator
        self.separator_to_sanitize: DirectorySeparator
        self.separator_sanitized, self.separator_to_sanitize = request.param
        self.sanitizer: PathSanitizer = PathSanitizer(self.separator_sanitized)

    def create_path_to_sanitize(self, *values: str) -> str:
        """
        Creates a path in "to sanitize" format using the `separator_to_sanitize`, it means the path
        is in its original format.

        Returns:
            str: The path to sanitize
        """
        separator: str = self.separator_to_sanitize.value
        value: str = separator.join(values)
        print(f"path_to_sanitize: {value}")
        return value

    def create_path_sanitized(self, *values: str) -> str:
        """
        Creates a path in "sanitized" format using the `separator_sanitized`, it means the path
        is in its final format.

        Returns:
            str: The path sanitized
        """
        separator: str = self.separator_sanitized.value
        value: str = separator.join(values)
        print(f"path_sanitized: {value}")
        return value

    def test_sanitize__explicit_false_and_dont_remove_start_directory_separator_and_path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize(None, False) == ""

    def test_sanitize__explicit_false_and_dont_remove_start_directory_separator_and_path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize("", False) == ""
        assert self.sanitizer.sanitize(" ", False) == ""

    def test_sanitize__explicit_false_and_dont_remove_start_directory_separator_and_path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.sanitize(self.create_path_to_sanitize(""), False) == ""
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", ""), False) == ""
        assert self.sanitizer.sanitize("1", False) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", ""), False) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", ""), False) == self.create_path_sanitized("", "1")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2"), False) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", ""), False) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", ""), False) == self.create_path_sanitized("", "1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2"), False) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", ""), False) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", ""), False) == self.create_path_sanitized("", "1", "2")

    def test_sanitize__implicit_false_and_dont_remove_start_directory_separator_and_path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize(None) == ""

    def test_sanitize__implicit_false_and_dont_remove_start_directory_separator_and_path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize("") == ""
        assert self.sanitizer.sanitize(" ") == ""

    def test_sanitize__implicit_false_and_dont_remove_start_directory_separator_and_path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("")) == ""
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "")) == ""
        assert self.sanitizer.sanitize("1") == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "")) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "")) == self.create_path_sanitized("", "1")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", "")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", "")) == self.create_path_sanitized("", "1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", "")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", "")) == self.create_path_sanitized("", "1", "2")

    def test_sanitize__remove_start_directory_separator_and_path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize(None, True) == ""

    def test_sanitize__remove_start_directory_separator_and_path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.sanitize("", True) == ""
        assert self.sanitizer.sanitize(" ", True) == ""

    def test_sanitize__remove_start_directory_separator_and_path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.sanitize(self.create_path_to_sanitize(""), True) == ""
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", ""), True) == ""
        assert self.sanitizer.sanitize("1", True) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", ""), True) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", ""), True) == "1"
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2"), True) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", ""), True) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", ""), True) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2"), True) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("1", "2", ""), True) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.sanitize(self.create_path_to_sanitize("", "1", "2", ""), True) == self.create_path_sanitized("1", "2")

    def test_concat__arguments_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.concat(None) == ""

    def test_concat__arguments_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.concat("") == ""
        assert self.sanitizer.concat(" ") == ""

    def test_concat__arguments_has_null_and_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.concat(None, "") == ""
        assert self.sanitizer.concat(None, " ") == ""
        assert self.sanitizer.concat("", None) == ""
        assert self.sanitizer.concat("", " ") == ""
        assert self.sanitizer.concat(" ", None) == ""
        assert self.sanitizer.concat(" ", "") == ""
        assert self.sanitizer.concat("", " ", None) == ""

    def test_concat__arguments_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.concat("1") == "1"
        assert self.sanitizer.concat("1", "") == "1"
        assert self.sanitizer.concat("", "1") == self.create_path_sanitized("", "1")
        assert self.sanitizer.concat("", "1", "") == self.create_path_sanitized("", "1")
        assert self.sanitizer.concat("1", None) == "1"
        assert self.sanitizer.concat("", "1", "") == self.create_path_sanitized("", "1")
        assert self.sanitizer.concat("", "1", None) == self.create_path_sanitized("", "1")
        assert self.sanitizer.concat("1", "2") == self.create_path_sanitized("1", "2")
        assert self.sanitizer.concat("1", "2", "") == self.create_path_sanitized("1", "2")
        assert self.sanitizer.concat("", "1", "2") == self.create_path_sanitized("", "1", "2")
        assert self.sanitizer.concat("", "1", "2", "") == self.create_path_sanitized("", "1", "2")
        assert self.sanitizer.concat(self.create_path_to_sanitize("1", ""), self.create_path_to_sanitize("2", "")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.concat(self.create_path_to_sanitize("1", ""), self.create_path_to_sanitize("2", ""), "") == self.create_path_sanitized("1", "2")
        assert self.sanitizer.concat("", self.create_path_to_sanitize("1", ""), self.create_path_to_sanitize("2", "")) == self.create_path_sanitized("", "1", "2")
        assert self.sanitizer.concat("", self.create_path_to_sanitize("1", ""), self.create_path_to_sanitize("2", ""), "") == self.create_path_sanitized("", "1", "2")

    def test_get_parent__path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.get_parent(None) == ""

    def test_get_parent__path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.get_parent("") == ""
        assert self.sanitizer.get_parent(" ") == ""

    def test_get_parent__path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.get_parent(self.separator_sanitized.value) == ""
        assert self.sanitizer.get_parent("1") == ""
        assert self.sanitizer.get_parent(PathSanitizerTests.FILE_NAME_TO_TEST) == ""
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "")) == ""
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "")) == ""
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2")) == "1"
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", PathSanitizerTests.FILE_NAME_TO_TEST)) == "1"
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2", "")) == self.create_path_sanitized("1")
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2", "")) == self.create_path_sanitized("1")
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2", "3")) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2", PathSanitizerTests.FILE_NAME_TO_TEST)) == self.create_path_sanitized("1", "2")
        assert self.sanitizer.get_parent(self.create_path_to_sanitize("1", "2", "3", "")) == self.create_path_sanitized("1", "2")

    def test_get_ame__path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.get_name(None) == ""

    def test_get_name__path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.get_name("") == ""
        assert self.sanitizer.get_name(" ") == ""

    def test_get_name__path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.get_name(self.create_path_to_sanitize(PathSanitizerTests.FILE_NAME_TO_TEST)) == PathSanitizerTests.FILE_NAME_TO_TEST
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", PathSanitizerTests.FILE_NAME_TO_TEST)) == PathSanitizerTests.FILE_NAME_TO_TEST
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "2", PathSanitizerTests.FILE_NAME_TO_TEST)) == PathSanitizerTests.FILE_NAME_TO_TEST
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1")) == "1"
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "2")) == "2"
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "2", "3")) == "3"
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "")) == "1"
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "2", "")) == "2"
        assert self.sanitizer.get_name(self.create_path_to_sanitize("1", "2", "3", "")) == "3"

    def test_add_directory_separator__path_is_null__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.add_directory_separator(None) == ""

    def test_add_directory_separator__path_is_empty__then_return_string_empty(
        self
    ) -> None:
        assert self.sanitizer.add_directory_separator("") == self.create_path_sanitized("")
        assert self.sanitizer.add_directory_separator(" ") == self.create_path_sanitized("")

    def test_add_directory_separator__path_is_reported__then_return_string(
        self
    ) -> None:
        assert self.sanitizer.add_directory_separator("1") == self.create_path_sanitized("1", "")
        assert self.sanitizer.add_directory_separator(self.create_path_to_sanitize("1", "2")) == self.create_path_sanitized("1", "2", "")
        assert self.sanitizer.add_directory_separator(self.create_path_to_sanitize("1", "2", "3")) == self.create_path_sanitized("1", "2", "3", "")
        assert self.sanitizer.add_directory_separator(self.create_path_to_sanitize("", "1")) == self.create_path_sanitized("", "1", "")
        assert self.sanitizer.add_directory_separator(self.create_path_to_sanitize("", "1", "2")) == self.create_path_sanitized("", "1", "2", "")
        assert self.sanitizer.add_directory_separator(self.create_path_to_sanitize("", "1", "2", "3")) == self.create_path_sanitized("", "1", "2", "3", "")