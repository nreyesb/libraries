# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the Hasher SHA for testing purpose.

Classes:
    - Sha1HasherTests (sha1_hasher_tests.py): The implementation for hasher SHA1 testing
    - Sha256HasherTests (sha256_hasher_tests.py): The implementation for hasher SHA256 testing
    - Sha512HasherTests (sha512_hasher_tests.py): The implementation for hasher SHA512 testing
"""
from .sha1_hasher_tests import Sha1HasherTests as Sha1HasherTests
from .sha256_hasher_tests import Sha256HasherTests as Sha256HasherTests
from .sha512_hasher_tests import Sha512HasherTests as Sha512HasherTests
