# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
# pylint: disable=unsubscriptable-object
# flake8: noqa F501
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: sha1_hasher_tests.py
Author: Toku Dev
"""
from overrides import override
from tests.toku.hasher.api import HasherTest
from toku.hasher.sha import Sha1Hasher


class Sha1HasherTests(HasherTest[Sha1Hasher]):
    """
    Provides test cases for Sha1Hasher class.
    """

    @override
    def _create_hasher(self) -> Sha1Hasher:
        return Sha1Hasher()

    @override
    def _create_plain_vs_hasher_texts(self) -> dict[str, str]:
        return {
            "i am a simple plaintext": "97cddaa8b6c872874e9c3cf019e2d99733826e2b",
            "i'am a special plaintext áéíóíúäëïöü": "91157924ff613bea6a2176332e4cbd3b1cf601b3",
        }
