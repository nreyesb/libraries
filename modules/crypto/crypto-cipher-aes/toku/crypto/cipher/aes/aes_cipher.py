# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: aes_cipher.py
Author: Toku
"""
from typing import final
from Crypto.Cipher import AES
from overrides import override
from toku.crypto.cipher.api import Cipher


@final
class AesCipher(Cipher):
    """
    Provides an AES implementation for encryption and decryption.
    """

    DEFAULT_ENCODING = "UTF-8"

    def __init__(self, key: bytes) -> None:
        """
        Initializes the AesCipher instance with the provided key.

        The process uses GCM mode for encryption and decryption processes
        because it allows to generate a totally different value for the same
        plaintext every time it's encrypted, because an internal random value
        is used which is part of the ciphertext, so it allows to have a more
        secure ciphertext and it's not a problem the decryption because the
        alghoritm already know how to get this random value from the ciphertext
        to use it during decryption.

        The process always considers to use UTF-8.

        For example:

        The key `s7dfjy987asdigh9` with the plaintext 'i am a plaintext' will
        generate:

        1. 'a9s87dtoiygasjdghjasokjgd' the first time is called
        2. '79ad867f45ad498e7as6f54as' the second time is called

        But the decryption process will generate 'i am a plaintext' for both
        cases.

        Args:
            key (bytes):
                The AES encryption/decryption key for symmetric cipher.

                - 16 (AES-128)
                - 24 (AES-192)
                - 32 (AES-256)
        """
        self._key: bytes = key

    @override
    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = AES.new(self._key, AES.MODE_GCM)
        ciphertext: bytes
        tag: bytes
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return bytes(cipher.nonce) + ciphertext + tag

    @override
    def decrypt(self, ciphertext: bytes) -> bytes:
        nonce: bytes = ciphertext[:16]
        tag: bytes = ciphertext[-16:]
        ciphertext_bytes = ciphertext[16:-16]
        cipher = AES.new(self._key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext_bytes, tag)
