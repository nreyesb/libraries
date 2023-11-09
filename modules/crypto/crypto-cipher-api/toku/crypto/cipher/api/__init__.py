# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the Cipher API.

Classes:
    - Cipher (cipher.py): The contract for cipher process
    - CipherException (cipher_exception.py): The common cipher exception
"""
from .cipher import Cipher as Cipher
from .cipher_exception import CipherException as CipherException
