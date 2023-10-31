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

Module: aes_cipher_tests.py
Author: Toku Dev
"""
from overrides import override
from tests.toku.crypto.cipher.api import CipherTest
from toku.crypto.cipher.aes import AesCipher


class AesCipherTests(CipherTest[AesCipher]):
    """
    Provides test cases for AesCipher class.
    """

    @override
    def _create_cipher(self) -> AesCipher:
        return AesCipher(bytes("ak58fj287fivk287", "utf-8"))

    @override
    def _create_plain_texts(self) -> list[str]:
        return [
            "i am a simple plaintext",
            "i'am a special plaintext áéíóíúäëïöü"
        ]

    @override
    def _create_cipher_vs_plain_texts(self) -> dict[str, str]:
        return {
            "9206d5e0b611aaf37f87d05eac12f958a7c0fe90506e7d77c2f9ee1ba5dd9c61824915f3d16ce220f6649259cb950e5c7684ab44cfff7b": "i am a simple plaintext",
            "7add48150a3d3600635c80ba66abe431606f79923aa3d4b55cae8d9fe89af3f129c4eaee547bbc8d9a26dc897e95858d4fd48b57c0bfac5a24c5656a3098fa526453fc922cec79e1f61d3e2025578e": "i'am a special plaintext áéíóíúäëïöü",
        }
