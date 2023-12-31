# Cipher AES

This library aims to provide the implementation to use cryptography Cipher AES.

## Works with

### As Library

Projects without poetry o for the local environment:

```bash
pip install toku-crypto-cipher-aes@{version}
```

Projects with poetry:

```bash
poetry add toku-crypto-cipher-aes@{version}
```

The following command is useful to install the dependency in the poetry virtual environment for new version in progress, that means the library is not available in the remote repository for dowloanding but the code is available to build the dist or the dist is available in the local machine. It's important remember to run the command in the environment where the dependency is required and just add the dependency manually or change the version number in the pyproject.toml file, on that way it's not needed to use editable mode or path dependency in poetry:

```bash
poetry run python -m pip install {artifact_path}
```

#### Usage

##### Configuration

The library doesn't require any specific configuration to use it.

##### Example

To use the library, you can import it in your Python code:

```python
# string
from toku.crypto.cipher.api import Cipher # optional, if not needed, just remove Cipher type hint or put AesCipher
from toku.crypto.cipher.aes import AesCipher

key: str = "" # see the documentation of the class
cipher: Cipher = AesCipher(key)
ciphertext: str = cipher.encrypt("my_text", "UTF-8")
plaintext: str = cipher.decrypt(ciphertext, "UTF-8")

print(ciphertext)
print(plaintext)
```

```python
# bytes
from toku.crypto.cipher.api import Cipher # optional, if not needed, just remove Cipher type hint or put AesCipher
from toku.crypto.cipher.aes import AesCipher

key: str = "" # see the documentation of the class
cipher: Cipher = AesCipher(key)
ciphertext: bytes = cipher.encrypt(b"my_text")
plaintext: bytes = cipher.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
```

### As Project

Install with poetry.lock or create it automatically if it doesn't exists:

```bash
poetry install
```

To update the poetry.lock if pyproject.toml is modified or the file is outdated:

```bash
poetry update
```

To recreate the poetry.lock:

```bash
poetry lock
```

Check the integrity of the poetry.lock file with pyproject.toml file:

```bash
poetry check
```

Check the integrity of the source code with mypy:

```bash
poetry run mypy .
```

Get the environment path after installation, which can be used in an IDE or Code Editor to set the interpreter:

```bash
poetry env info --path
```

You can run the tests using:

```bash
# -v is for verbose output
# --cov is for coverage
# --cov-fail-under=MIN to set the minimum needed
# -n {NUM} to run in differents workers in parallel

poetry run pytest -n {WORKERS} -v --cov --cov-fail-under={MIN}
```

## About

Refers to **pyproject.toml** for information about:

- License
- Authors
- References and Resources
    - Homepage
    - Documentation
