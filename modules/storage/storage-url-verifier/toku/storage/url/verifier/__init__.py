# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
# flake8: noqa F401
"""
This package provides the StorageUrl Verifier.

Classes:
    - StorageUrlVerificationException (storage_url_verification_exception.py): The storage url verification exception
    - Verification (verification.py): The verification
"""
from .storage_url_verification_exception import StorageUrlVerificationException as StorageUrlVerificationException
from .verification import Verification as Verification
