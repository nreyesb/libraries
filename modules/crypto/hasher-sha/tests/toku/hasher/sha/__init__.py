"""
This package provides the Hasher SHA for testing purpose.

Classes:
    - Sha1HasherTests (sha1_hasher_tests.py): The definitions for hasher SHA1 testing
    - Sha256HasherTests (sha256_hasher_tests.py): The definitions for hasher SHA256 testing
    - Sha512HasherTests (sha512_hasher_tests.py): The definitions for hasher SHA512 testing
"""
# pylint: disable=useless-import-alias
# flake8: noqa F401
from .sha1_hasher_tests import Sha1HasherTests as Sha1HasherTests
from .sha256_hasher_tests import Sha256HasherTests as Sha256HasherTests
from .sha512_hasher_tests import Sha512HasherTests as Sha512HasherTests
