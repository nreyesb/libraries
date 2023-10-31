# -*- coding: utf-8 -*-
# flake8: noqa: E501
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
prior written permission from Your Company Name.

Module: sha512_hasher_tests.py
Author: Toku Dev
"""
from typing import final
from overrides import override
from tests.toku.crypto.hasher.api import HasherTest
from toku.crypto.hasher.sha import Sha512Hasher


@final
class Sha512HasherTests(HasherTest[Sha512Hasher]):
    """
    Provides test cases for Sha512Hasher class.
    """

    @override
    def _create_hasher(self) -> Sha512Hasher:
        return Sha512Hasher()

    @override
    def _create_plain_vs_hasher_texts(self) -> dict[str, str]:
        return {
            "i am a simple plaintext": "095140e024fd19959d93e043826b83ce17931fd4ad8ef5f88b64dda1a017f7bf85e610e7943f20d71bdb9701235ede7d4eda5b900664980526f56f7bd953767b",
            "i'am a special plaintext áéíóíúäëïöü": "dcfa9a041894bed5cb34e2d3b5bffaed2675c4525e3aacd0fbf9c160f1c8f7df21bcc1a031eb2a7257d118fff413969e0f87df0b2952783f584960c32966f47e",
        }
