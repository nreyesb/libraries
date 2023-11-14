# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the common mappers.

Classes:
    - SingleMapper (single_mapper.py): The single mapper to convert T in M
    - DoubleMapper (double_mapper.py): The double mapper to convert T in M and vice versa
"""
from .single_mapper import SingleMapper as SingleMapper
from .double_mapper import DoubleMapper as DoubleMapper
