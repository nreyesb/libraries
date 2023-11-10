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

Module: sha512_hasher_tests.py
Author: Toku
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

    UTF8_ENCODING = "UTF-8"
    LATIN1_ENCODING = "ISO-8859-1"

    @override
    def _create_hasher(self) -> Sha512Hasher:
        return Sha512Hasher()

    @override
    def _create_hasher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        return [
            (
                b'\tQ@\xe0$\xfd\x19\x95\x9d\x93\xe0C\x82k\x83\xce\x17\x93\x1f\xd4\xad\x8e\xf5\xf8\x8bd\xdd\xa1\xa0\x17\xf7\xbf\x85\xe6\x10\xe7\x94? \xd7\x1b\xdb\x97\x01#^\xde}N\xda[\x90\x06d\x98\x05&\xf5o{\xd9Sv{',
                bytes("i am a simple plaintext", Sha512HasherTests.UTF8_ENCODING)
            ),
            (
                b'\xdc\xfa\x9a\x04\x18\x94\xbe\xd5\xcb4\xe2\xd3\xb5\xbf\xfa\xed&u\xc4R^:\xac\xd0\xfb\xf9\xc1`\xf1\xc8\xf7\xdf!\xbc\xc1\xa01\xeb*rW\xd1\x18\xff\xf4\x13\x96\x9e\x0f\x87\xdf\x0b)Rx?XI`\xc3)f\xf4~',
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha512HasherTests.UTF8_ENCODING)
            ),
            (
                b'\tQ@\xe0$\xfd\x19\x95\x9d\x93\xe0C\x82k\x83\xce\x17\x93\x1f\xd4\xad\x8e\xf5\xf8\x8bd\xdd\xa1\xa0\x17\xf7\xbf\x85\xe6\x10\xe7\x94? \xd7\x1b\xdb\x97\x01#^\xde}N\xda[\x90\x06d\x98\x05&\xf5o{\xd9Sv{',
                bytes("i am a simple plaintext", Sha512HasherTests.LATIN1_ENCODING)
            ),
            (
                b'\xf7\x07\xcdg\xf5\x13\xd6\xd4\xb6\xe19j\x83\x91\\\xd5\x9d\xa8R\xda\xdd\x81\x90\x03[\xf8n\x16?\xeb\xe6\xd8\x1c\x82\xd4e\xae\xfe\xc3N\x04g\xfb\xcc7/\x82\x9e\x1a\xcc\x0c\x14 \xad)g\xd49\xf7\x17\x85$\x8e\x00',
                bytes("i'am a special plaintext áéíóíúäëïöü", Sha512HasherTests.LATIN1_ENCODING)
            )
        ]

    @override
    def _create_hasher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        return [
            (
                "095140e024fd19959d93e043826b83ce17931fd4ad8ef5f88b64dda1a017f7bf85e610e7943f20d71bdb9701235ede7d4eda5b900664980526f56f7bd953767b",
                "i am a simple plaintext",
                Sha512HasherTests.UTF8_ENCODING
            ),
            (
                "dcfa9a041894bed5cb34e2d3b5bffaed2675c4525e3aacd0fbf9c160f1c8f7df21bcc1a031eb2a7257d118fff413969e0f87df0b2952783f584960c32966f47e",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha512HasherTests.UTF8_ENCODING
            ),
            (
                "095140e024fd19959d93e043826b83ce17931fd4ad8ef5f88b64dda1a017f7bf85e610e7943f20d71bdb9701235ede7d4eda5b900664980526f56f7bd953767b",
                "i am a simple plaintext",
                Sha512HasherTests.LATIN1_ENCODING
            ),
            (
                "f707cd67f513d6d4b6e1396a83915cd59da852dadd8190035bf86e163febe6d81c82d465aefec34e0467fbcc372f829e1acc0c1420ad2967d439f71785248e00",
                "i'am a special plaintext áéíóíúäëïöü",
                Sha512HasherTests.LATIN1_ENCODING
            )
        ]
