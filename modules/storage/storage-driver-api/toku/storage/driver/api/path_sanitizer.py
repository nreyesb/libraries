# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: path_sanitizer.py
Author: Toku
"""
from typing import Optional
from toku.storage.driver.api import DirectorySeparator


class PathSanitizer:
    """
    Provides the sanitizer processes for a path.
    """

    def __init__(self, separator: DirectorySeparator) -> None:
        """
        Instantiates a new path sanitizer.

        Args:
            separator (DirectorySeparator): The directory separator.
        """
        self._separator: DirectorySeparator = separator

    def sanitize(self, path: Optional[str], remove_start_directory_separator: bool = False) -> str:
        """
        Provides the process to create a path consistent.

        If the path is None, return an empty string.

        Apply strip to the path.

        Delete the start character of the path if and only if it is equal to / or \\ and
        `remove_start_directory_separator` is True.

        Delete the last character of the path if and only if it is equal to / or \\.

        Process the path keeping the separator consistent according to `separator`.

        Args:
            path (Optional[str]): The path.
            remove_start_directory_separator (bool): Indicates if the start separator has
                                                     to be removed.

        Returns:
            str: The processed path.
        """
        if not path or not path.strip():
            return ""

        path = path.strip()

        if remove_start_directory_separator:
            path = PathSanitizer._remove_start(path, DirectorySeparator.SLASH.value)
            path = PathSanitizer._remove_start(path, DirectorySeparator.BACKSLASH.value)

        path = PathSanitizer._remove_end(path, DirectorySeparator.SLASH.value)
        path = PathSanitizer._remove_end(path, DirectorySeparator.BACKSLASH.value)

        path = path.replace(DirectorySeparator.SLASH.value, self._separator.value)
        path = path.replace(DirectorySeparator.BACKSLASH.value, self._separator.value)

        return path

    def concat(self, *values: Optional[str]) -> str:
        """
        Concatenate the values using separator, each value is
        sanitized with `sanitize` and the final result as well.

        If the values are None, return an empty string.

        Args:
            values (Optional[str]): The values to concatenate.

        Returns:
            str: The values concatenated and sanitized.
        """
        sanitized_values: list[str] = [
            self.sanitize(value) for value in values if value is not None
        ]
        return self.sanitize(self._separator.value.join(sanitized_values))

    def get_parent(self, path: Optional[str]) -> str:
        """
        Get the parent directory of the path after it has been sanitized with
        `sanitize`.

        If the path is None or blank, return an empty string.

        It uses a split with :-1 and after that a join using the `_separator` to
        get the parent directory name because os.dirname works with the native
        directory separator

        Args:
            path (Optional[str]): The path.

        Returns:
            str: The parent folder.
        """
        if not path or not path.strip():
            return ""

        return self._separator.value.join(self.sanitize(path).split(self._separator.value)[:-1])

    def get_name(self, path: Optional[str]) -> str:
        """
        Get the name of the path after it has been sanitized with
        `sanitize`.

        If the path is None or blank, return an empty string.

        It uses a split with -1 to get the filename because os.basename works
        with the native directory separator

        Args:
            path (Optional[str]): The path.

        Returns:
            str: The name.
        """
        if not path or not path.strip():
            return ""

        return self.sanitize(path).split(self._separator.value)[-1]

    def add_directory_separator(self, path: Optional[str]) -> str:
        """
        Add the separator to the end of the path after applying the
        `sanitize`.

        If the path is None or blank, return an empty string.

        Args:
            path (Optional[str]): The path.

        Returns:
            str: The parent folder.
        """
        if not path or not path.strip():
            return ""

        return f"{self.sanitize(path)}{self._separator.value}"

    @staticmethod
    def _remove_start(text: str, start_text: str) -> str:
        """
        Remove the start_text from the text if it starts with that text.

        Args:
            text (str): The text.
            start_text (str): The start text.

        Returns:
            str: The string.
        """
        text = ("" if not text else text).strip()

        if text.startswith(start_text):
            return text[len(start_text):]

        return text

    @staticmethod
    def _remove_end(text: str, end_text: str) -> str:
        """
        Remove the end_text from the text if it ends with that text.

        Args:
            text (str): The text.
            end_text (str): The end text.

        Returns:
            str: The string.
        """
        text = ("" if not text else text).strip()

        if text.endswith(end_text):
            return text[: -len(end_text)]

        return text
