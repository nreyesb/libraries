# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Your Company Name.

Module: aes_cipher.py
Author: Toku Dev
"""
from typing import Optional
from Crypto.Cipher import AES
from overrides import override
from toku.crypto.cipher.api import Cipher


class AesCipher(Cipher):
    """
    Provides an AES implementation for encryption and decryption.
    """

    def __init__(self, key: bytes) -> None:
        """
        Initializes the AesCipher instance with the provided key.

        Args:
            key (bytes):
                The AES encryption/decryption key for symmetric cipher.

                - 16 (AES-128)
                - 24 (AES-192)
                - 32 (AES-256)
        """
        self.key: bytes = key

    @override
    def encrypt(self, plaintext: Optional[str]) -> str:
        if not plaintext:
            return ""

        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext: bytes
        tag: bytes
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        encrypted_bytes: bytes = bytes(cipher.nonce) + ciphertext + tag
        return encrypted_bytes.hex()

    @override
    def decrypt(self, ciphertext: Optional[str]) -> str:
        if not ciphertext:
            return ""

        ciphertext_bytes: bytes = bytes.fromhex(ciphertext)
        nonce: bytes = ciphertext_bytes[:16]
        tag: bytes = ciphertext_bytes[-16:]
        ciphertext_bytes = ciphertext_bytes[16:-16]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        decrypted: bytes = cipher.decrypt_and_verify(ciphertext_bytes, tag)
        return decrypted.decode()
