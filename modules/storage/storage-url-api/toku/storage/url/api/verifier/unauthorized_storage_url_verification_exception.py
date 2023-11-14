# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: unauthorized_storage_url_verification_exception.py
Author: Toku
"""
from toku.storage.url.verifier.api import StorageUrlVerificationException


class UnauthorizedStorageUrlVerificationException(StorageUrlVerificationException):
    """
    Represents a UnauthorizedStorageUrlVerificationException exception.
    """
