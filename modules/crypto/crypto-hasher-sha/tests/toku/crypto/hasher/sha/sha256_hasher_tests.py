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

Module: sha256_hasher_tests.py
Author: Toku Dev
"""
from overrides import override
from tests.toku.crypto.hasher.api import HasherTest
from toku.crypto.hasher.sha import Sha256Hasher


class Sha256HasherTests(HasherTest[Sha256Hasher]):
    """
    Provides test cases for Sha256Hasher class.
    """

    @override
    def _create_hasher(self) -> Sha256Hasher:
        return Sha256Hasher()

    @override
    def _create_plain_vs_hasher_texts(self) -> dict[str, str]:
        return {
            "i am a simple plaintext": "7a70aeac1144e3ce723a6de73dd351f7b03c577f668280472d9183ff58fd4373",
            "i'am a special plaintext áéíóíúäëïöü": "dffb9b44251c870997998b05e03d6cba5905a0abaf17f34cead287219f386576",
        }
