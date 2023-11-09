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

Module: aes_cipher_tests.py
Author: Toku
"""
import base64
from dataclasses import dataclass
from datetime import datetime
import pickle
from overrides import override
from tests.toku.crypto.cipher.api import CipherTest
from toku.crypto.cipher.aes import AesCipher

@dataclass
class MyClass:
    """
    This class was used to generate a bytes array to test
    a non-string input.
    """
    attr1: int = 68543
    attr2: str = "asdd542as48sa6d87-a-e-o-iáéóí~u`¨"
    attr3: datetime = datetime.utcnow()


class AesCipherTests(CipherTest[AesCipher]):
    """
    Provides test cases for AesCipher class.
    """

    UTF8_ENCODING = "UTF-8"
    LATIN1_ENCODING = "ISO-8859-1"

    @override
    def _create_cipher(self) -> AesCipher:
        return AesCipher(bytes("ak58fj287fivk287", "utf-8"))

    @override
    def _create_plain_texts_for_bytes(self) -> list[bytes]:
        return [
            bytes("i am a simple plaintext", AesCipherTests.UTF8_ENCODING),
            bytes("i'am a special plaintext áéíóíúäëïöü", AesCipherTests.UTF8_ENCODING),
            bytes("i am a simple plaintext", AesCipherTests.LATIN1_ENCODING),
            bytes("i'am a special plaintext áéíóíúäëïöü", AesCipherTests.LATIN1_ENCODING)
        ]

    @override
    def _create_cipher_vs_plain_texts_for_bytes(self) -> list[tuple[bytes, bytes]]:
        return [
            (
                b'\xd9\x85\\\x98\xb8\xf6\x91\xfcw\x19\x99\xc5t\x02"\x01\xa9\x19\xe687\xc2\xc9\x94\x89@\xb8)\xe4f\xe7\xe91\xe0\x03\x80\xbf\xd0\xfe\xa1\xa2B\x8c\xd8m\x99a\xcd\xecd\xfa\x08\xa9\xa0\x02',
                bytes("i am a simple plaintext", AesCipherTests.UTF8_ENCODING)
            ),
            (
                b'N2\x91\xe6\xf0\xa5j\xd9\xa7\xa7\xc4\xb6\xedBx\xd4eXh_\x88\xb2d\x15\x80\xa1\xbc\xd6~hL\xb8\xa0\xab\x86\xde)W\x8b`\x9dV6g.\xf1+\x11\xd3\x82\xe0\xf1\x14Y\xdce\xf9E\xb3i\x04\x1c\x07\x0f\xf1-\xba\xef\xf3\xcd\xb6%\xe5\x06vi\x06\x93\x9e',
                bytes("i'am a special plaintext áéíóíúäëïöü", AesCipherTests.UTF8_ENCODING)
            ),
            (
                b'\xd9\x10\x0f\xd6\xc8\xe8!\\)\x89O\x0cgHK\x8bI\xa7\xa9\xf5v5\xf8\xf6\xa4(c-\x17u\xc1\xf4%-\xe8\xc3\xb3_\xc0-t \xc5o\xe6\t+\xd1\x81\xfc\x991Rg\xe5',
                bytes("i am a simple plaintext", AesCipherTests.LATIN1_ENCODING)
            ),
            (
                b'\x8a\xf2\x16j\x8d\xc0\x19C7.\xb3*\xfd<\x1d\x95\xf11\x18D\xda\xe6\xc1)`\x9a\xbc-\xdb\xd5\x87\xe9Nb\xfc\x0f-\xf0\x82N\xf04\xea9\x0b\xc0\xcaV"\xf4\xebeQ\x13\x89\x9dT%\xa6l\xc1\x93\xe9\xab\x8c@=\x15',
                bytes("i'am a special plaintext áéíóíúäëïöü", AesCipherTests.LATIN1_ENCODING)
            ),
            ( # correspondes to MyClass as bytes
                b'\xeb\xf9O[\x82\x80i\x000\x94\xaa\x90\xbc\xc7\x1b\x15h$k\xa7\xc9\x10\x14q\xac\xff8,\xcd"%i\xddwnK\xd5IM*$\xdf\xa2s(\x17\xa8\xdf\xa0 D\xe4n{h\xa8h\xbe>\xaa@F]\xed\xc6-\xcc\xf4qO\x91\xe5l\x0b l\xdc\x13\x11 8\t\xd1\x88j\xa5\xbd\xb7\xe2\n:\x18\x81\x15\xf6\xfe^\x86\xec\xbd\x8d\x00kO\xb9\x9ch\xc3;\xf3\xee\xb47\xed\xad\xa4\xa5%\x1c\'\x06z7f\xb47\xa4v\xc1\x8cBxP\x12\xda\xd6\x9a\xec\xf6\xf5\x91\xebd-\xddX\xd3%if9\xd1\xa4\x1ac\x11?\x1c\xf8K\x914\xd3b\xdc\xe6\xaa\xaf\xc3\xa6\xea\xb9\xee\x9f\xf8\xe2\x95\x8b\x05\x16\x94\xd1\xcf\xcdb\x1d\x04\xd4\xb1\xf6a\x10\xd5\x08\x07eu\x91',
                b'\x80\x04\x95\x9b\x00\x00\x00\x00\x00\x00\x00\x8c\x14aes.aes_cipher_tests\x94\x8c\x07MyClass\x94\x93\x94)\x81\x94}\x94(\x8c\x05attr1\x94J\xbf\x0b\x01\x00\x8c\x05attr2\x94\x8c&asdd542as48sa6d87-a-e-o-i\xc3\xa1\xc3\xa9\xc3\xb3\xc3\xad~u`\xc2\xa8\x94\x8c\x05attr3\x94\x8c\x08datetime\x94\x8c\x08datetime\x94\x93\x94C\n\x07\xe7\x0b\t\x14\x1b\x1d\x02\xbc \x94\x85\x94R\x94ub.'
            )
        ]

    @override
    def _create_plain_texts_for_string(self) -> list[tuple[str, str]]:
        return [
            (
                "i am a simple plaintext",
                AesCipherTests.UTF8_ENCODING
            ),
            (
                "i'am a special plaintext áéíóíúäëïöü",
                AesCipherTests.UTF8_ENCODING
            ),
            (
                "i am a simple plaintext",
                AesCipherTests.LATIN1_ENCODING
            ),
            (
                "i'am a special plaintext áéíóíúäëïöü",
                AesCipherTests.LATIN1_ENCODING
            )
        ]

    @override
    def _create_cipher_vs_plain_texts_for_string(self) -> list[tuple[str, str, str]]:
        return [
            (
                "9206d5e0b611aaf37f87d05eac12f958a7c0fe90506e7d77c2f9ee1ba5dd9c61824915f3d16ce220f6649259cb950e5c7684ab44cfff7b",
                "i am a simple plaintext",
                AesCipherTests.UTF8_ENCODING
            ),
            (
                "7add48150a3d3600635c80ba66abe431606f79923aa3d4b55cae8d9fe89af3f129c4eaee547bbc8d9a26dc897e95858d4fd48b57c0bfac5a24c5656a3098fa526453fc922cec79e1f61d3e2025578e",
                "i'am a special plaintext áéíóíúäëïöü",
                AesCipherTests.UTF8_ENCODING
            ),
            (
                "514263a1361dd613a197aae3c5e14eee2e4eb6d63b8ac6261e36837376fa153927a3e49da201c64d1b1913fdb1184fabeaf0765f5d7b73",
                "i am a simple plaintext",
                AesCipherTests.LATIN1_ENCODING
            ),
            (
                "d914f63abefd3d13bb1f0cc6038365fc065f7af2b3bd6a3b7b340198636c38c93815b346c8b4344de9519083479e72c2f96872db2f931c15f51fdf3bb5df8d3b21aaf597",
                "i'am a special plaintext áéíóíúäëïöü",
                AesCipherTests.LATIN1_ENCODING
            ),
            ( # correspondes to MyClass as string, the bytes were encoded with base64 and decoded with UTF-8
                "2775d532c0ca00c1444cf4b6fd2f5b86077ced20b7a70d7797366ed04078208311658a12a07b6f498a1ca36e89e6a11acc0ef0414ef0e03620089398e2bfabe63c6d65feff430b11641f8b4f4f077984bdb04d03f7fed30b2a782d0940b5e6642421971d191f9d0c935534b7c83b6661072e99b144204410ec6ac2e7c268fbfea783e8843e69d6d5327ab8530851e39634ee291b24def4507d488dc2832d7763f3a8ac415e14bacff826a1502898cd0e71c5476150e1ef0fd8d72dcc4b4cad9d1eedf8b51bbfebbdc8ac8737ec55bed37a149257862383abe19bb2f49c7d06ec91a65049a5d6e8b97f5625612be2f33bc626362e00d2582f3351423ae52ff32d",
                "gASVmwAAAAAAAACMFGFlcy5hZXNfY2lwaGVyX3Rlc3RzlIwHTXlDbGFzc5STlCmBlH2UKIwFYXR0cjGUSr8LAQCMBWF0dHIylIwmYXNkZDU0MmFzNDhzYTZkODctYS1lLW8tacOhw6nDs8OtfnVgwqiUjAVhdHRyM5SMCGRhdGV0aW1llIwIZGF0ZXRpbWWUk5RDCgfnCwkUKiEEO6SUhZRSlHViLg==",
                AesCipherTests.UTF8_ENCODING
            )
        ]
