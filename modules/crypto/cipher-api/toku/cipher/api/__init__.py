"""
This package provides the Cipher API.

Classes:
    - Cipher (cipher.py): The definitions for cipher process
    - CipherException (cipher_exception.py): The common cipher exception
"""
# pylint: disable=useless-import-alias
# flake8: noqa F401
from .cipher import Cipher as Cipher
from .cipher_exception import CipherException as CipherException
