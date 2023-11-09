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

Module: storage_driver_test.py
Author: Toku
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from overrides import EnforceOverrides
from toku.storage.driver.api import StorageDriver

T = TypeVar("T", bound=StorageDriver)


class StorageDriverTest(ABC, EnforceOverrides, Generic[T]):
    """
    Provides the contract with the test cases for any kind StorageDriver class.
    """

    @abstractmethod
    def _initialize_test(self) -> None:
        """
        """

    @abstractmethod
    def _teardown_test(self) -> None:
        """
        """

    @abstractmethod
    def test_open__successful_driver_initialization__then_return_void(self) -> None:
        """
        """

    @abstractmethod
    def test_open__unsuccessful_driver_initialization__then_raise_exception(self) -> None:
        """
        """

    @abstractmethod
    def test_close__successful_driver_completion__then_return_void(self) -> None:
        """
        """

    @abstractmethod
    def test_get__file_not_exists__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get__file_is_directory__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get__file_is_root__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get__file_in_directory__then_return_optional_byte_array(self) -> None:
        """
        """

    @abstractmethod
    def test_get__file_in_root__then_return_optional_byte_array(self) -> None:
        """
        """

    @abstractmethod
    def test_get_as_input_stream__file_not_exists__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get_as_input_stream__file_is_directory__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get_as_input_stream__file_is_root__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get_as_input_stream__file_in_directory__then_return_optional_input_stream(self) -> None:
        """
        """

    @abstractmethod
    def test_get_as_input_stream__file_in_root__then_return_optional_input_stream(self) -> None:
        """
        """

    @abstractmethod
    def test_exists__file_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_exists__file_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_exists__file_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_exists__file_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_exists__file_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__byte_array__file_in_existing_file__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__byte_array__file_in_directory__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__byte_array__file_in_root__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__input_stream__file_in_existing_file__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__input_stream__file_in_directory__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__input_stream__file_in_root__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__path_as_string__file_in_existing_file__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__path_as_string__file_in_directory__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file__path_as_string__file_in_root__then_return_optional_string(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__byte_array__file_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__byte_array__file_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__byte_array__file_in_existing_file_as_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__byte_array__file_without_name__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__input_stream__file_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__input_stream__file_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__input_stream__file_in_existing_file_as_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__input_stream__file_without_name__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__path_as_string__file_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__path_as_string__file_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__path_as_string__file_in_existing_file_as_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_put_file_as__path_as_string__file_without_name__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_append__file_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_append__file_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_append__file_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_append__file_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_append__file_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__source_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__target_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__source_exists_and_target_is_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__target_is_file__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__another_storage_driver__target_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__another_storage_driver__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__another_storage_driver__source_exists_and_target_is_source__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__another_storage_driver__target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy__another_storage_driver__target_is_file__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__source_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__target_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__source_exists_and_target_is_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move__target_is_file__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move__another_storage_driver__target_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__another_storage_driver__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move__another_storage_driver__source_exists_and_target_is_source__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move__another_storage_driver__target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move__another_storage_driver__target_is_file__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_delete__file_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete__file_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete__file_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete__file_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__source_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__target_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__target_is_directory__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__source_exists_and_target_is_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename__source_exists_and_target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_files__directory_not_exists__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_files__directory_is_file__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_files__get__then_return_collection_string(self) -> None:
        """
        """

    @abstractmethod
    def test_all_files__directory_not_exists__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_all_files__directory_is_file__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_all_files__get__then_return_collection_string(self) -> None:
        """
        """

    @abstractmethod
    def test_directories__directory_not_exists__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_directories__directory_is_file__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_directories__get__then_return_collection_string(self) -> None:
        """
        """

    @abstractmethod
    def test_all_directories__directory_not_exists__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_all_directories__directory_is_file__then_return_collection_empty(self) -> None:
        """
        """

    @abstractmethod
    def test_all_directories__get__then_return_collection_string(self) -> None:
        """
        """

    @abstractmethod
    def test_exists_directory__directory_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_exists_directory__directory_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_exists_directory__directory_is_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_exists_directory__directory_in_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_exists_directory__directory_in_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__source_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__target_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__target_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__target_is_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__target_is_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__target_is_non_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__target_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__target_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__target_is_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__target_is_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_copy_directory__another_storage_driver__target_is_non_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__source_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__target_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__target_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__target_is_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__target_is_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__target_is_non_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__source_exists_and_target_is_parent_folder_of_source__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__source_exists_and_is_part_of_target_parent__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__target_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__target_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__target_is_root__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__target_is_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_move_directory__another_storage_driver__target_is_non_empty_directory__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_make_directory__directory_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_make_directory__directory_already_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_make_directory__directory_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_make_directory__directory_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_is_empty__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_has_file__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_delete_directory__directory_has_directories_and_files__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__source_not_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__source_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__source_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__target_exists__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__target_is_root__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__target_is_file__then_return_false(self) -> None:
        """
        """

    @abstractmethod
    def test_rename_directory__source_exists_and_target_not_exists__then_return_true(self) -> None:
        """
        """

    @abstractmethod
    def test_get_metadata__source_not_exists__then_return_optional_none(self) -> None:
        """
        """

    @abstractmethod
    def test_get_metadata__from_file__then_return_optional_metadata(self) -> None:
        """
        """

    @abstractmethod
    def test_get_metadata__from_folder__then_return_optional_metadata(self) -> None:
        """
        """

    @abstractmethod
    def test_get_metadata__from_root__then_return_optional_metadata(self) -> None:
        """
        """
