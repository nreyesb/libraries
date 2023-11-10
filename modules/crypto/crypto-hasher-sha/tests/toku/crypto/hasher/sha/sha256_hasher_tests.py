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

Module: sha256_hasher_tests.py
Author: Toku
"""
from typing import final
from overrides import override
from tests.toku.crypto.hasher.api import HasherTest
from toku.crypto.hasher.sha import Sha256Hasher


@final
class Sha256HasherTests(HasherTest[Sha256Hasher]):
    """
    Provides test cases for Sha256Hasher class.
    """

    UTF8_ENCODING = "UTF-8"
    LATIN1_ENCODING = "ISO-8859-1"

    @override
    def _create_hasher(self) -> Sha256Hasher:
        return Sha256Hasher()

    @override
    def _create_hasher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        return [
            (
                b'zp\xae\xac\x11D\xe3\xcer:m\xe7=\xd3Q\xf7\xb0<W\x7ff\x82\x80G-\x91\x83\xffX\xfdCs',
                bytes("i am a simple plaintext", Sha256HasherTests.UTF8_ENCODING)
            ),
            (
                b'\xdf\xfb\x9bD%\x1c\x87\t\x97\x99\x8b\x05\xe0=l\xbaY\x05\xa0\xab\xaf\x17\xf3L\xea\xd2\x87!\x9f8ev',
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha256HasherTests.UTF8_ENCODING)
            ),
            (
                b'zp\xae\xac\x11D\xe3\xcer:m\xe7=\xd3Q\xf7\xb0<W\x7ff\x82\x80G-\x91\x83\xffX\xfdCs',
                bytes("i am a simple plaintext", Sha256HasherTests.LATIN1_ENCODING)
            ),
            (
                b"\xc4.\xe5\x1e\xbaG\x0b\xabb\x90\xe1\xf6C\x03]\xf4\x07\xc9\xefq}\xc2\xf5\xc7\xdd\xe0\x92'\x94\xe2\xf1\xe7",
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha256HasherTests.LATIN1_ENCODING)
            )
        ]

    @override
    def _create_hasher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        return [
            (
                "7a70aeac1144e3ce723a6de73dd351f7b03c577f668280472d9183ff58fd4373",
                "i am a simple plaintext",
                Sha256HasherTests.UTF8_ENCODING
            ),
            (
                "dffb9b44251c870997998b05e03d6cba5905a0abaf17f34cead287219f386576",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha256HasherTests.UTF8_ENCODING
            ),
            (
                "7a70aeac1144e3ce723a6de73dd351f7b03c577f668280472d9183ff58fd4373",
                "i am a simple plaintext",
                Sha256HasherTests.LATIN1_ENCODING
            ),
            (
                "c42ee51eba470bab6290e1f643035df407c9ef717dc2f5c7dde0922794e2f1e7",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha256HasherTests.LATIN1_ENCODING
            )
        ]
