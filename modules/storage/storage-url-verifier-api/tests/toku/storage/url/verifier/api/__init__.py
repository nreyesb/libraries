# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the StorageUrl Verifier for testing purpose.

Classes:
    - ValidCase (verification_tests.py): Valid case to test
    - InvalidCase (verification_tests.py): Invalid case to test
    - VerificationTest (verification_tests.py): Url encoded tests
"""
from .verification_test import ValidCase as ValidCase
from .verification_test import InvalidCase as InvalidCase
from .verification_test import VerificationTest as VerificationTest
