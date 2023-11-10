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

Module: sha1_hasher_tests.py
Author: Toku
"""
from typing import final
from overrides import override
from tests.toku.crypto.hasher.api import HasherTest
from toku.crypto.hasher.sha import Sha1Hasher


@final
class Sha1HasherTests(HasherTest[Sha1Hasher]):
    """
    Provides test cases for Sha1Hasher class.
    """

    UTF8_ENCODING = "UTF-8"
    LATIN1_ENCODING = "ISO-8859-1"

    @override
    def _create_hasher(self) -> Sha1Hasher:
        return Sha1Hasher()

    @override
    def _create_hasher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        return [
            (
                b'\x97\xcd\xda\xa8\xb6\xc8r\x87N\x9c<\xf0\x19\xe2\xd9\x973\x82n+',
                bytes("i am a simple plaintext", Sha1HasherTests.UTF8_ENCODING)
            ),
            (
                b'\x91\x15y$\xffa;\xeaj!v3.L\xbd;\x1c\xf6\x01\xb3',
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha1HasherTests.UTF8_ENCODING)
            ),
            (
                b'\x97\xcd\xda\xa8\xb6\xc8r\x87N\x9c<\xf0\x19\xe2\xd9\x973\x82n+',
                bytes("i am a simple plaintext", Sha1HasherTests.LATIN1_ENCODING)
            ),
            (
                b'\xd8\xc8\xf2Y\x16\xb8\x96\xdd\x92\x94\x93`$\x06;_\xa2=F\xcd',
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha1HasherTests.LATIN1_ENCODING)
            )
        ]

    @override
    def _create_hasher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        return [
            (
                "97cddaa8b6c872874e9c3cf019e2d99733826e2b",
                "i am a simple plaintext",
                Sha1HasherTests.UTF8_ENCODING
            ),
            (
                "91157924ff613bea6a2176332e4cbd3b1cf601b3",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha1HasherTests.UTF8_ENCODING
            ),
            (
                "97cddaa8b6c872874e9c3cf019e2d99733826e2b",
                "i am a simple plaintext",
                Sha1HasherTests.LATIN1_ENCODING
            ),
            (
                "d8c8f25916b896dd9294936024063b5fa23d46cd",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha1HasherTests.LATIN1_ENCODING
            )
        ]
