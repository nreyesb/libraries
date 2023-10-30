# Cipher AES

This library aims to provide the implementation to use Cipher AES.

## Installation

You can install the library as dependency with:

```bash
# projects without poetry o for the local environment

pip install toku-cipher-aes@{version}
```

```bash
# projects with poetry

poetry add toku-cipher-aes@{version}
```

```bash
# useful to install the dependency in local environment for new version in progress, but remember to run the command in the environment where you need the dependency and just add the dependency manually or change the version number in the pyproject.toml file

poetry run python -m pip install {project_path}/{dist}/{artifact_name}
```

You can install the library as project with:

```bash
# install
poetry install

# check the integrity
poetry run mypy .
```

## Configuration

The library doesn't require any specific configuration to use it.

## Testing

You can run the tests using:

```bash
# -v is for verbos
# --cov is for coverage
# --cov-fail-under=MIN to set the minimum needed

poetry run pytest -v --cov --cov-fail-under=MIN
```

TODO: is it required? what do we need here?

For more information about testing and test coverage, please refer to [Testing Guide](docs/testing.md).

## Usage

To use the library, you can import it in your Python code:

```python
from toku.crypto.cipher.api import Cipher # optional, if not needed, just remove Cipher type hint or put AesCipher
from toku.crypto.cipher.aes import AesCipher

key: str = "" # see the documentation of the class
cipher: Cipher = AesCipher(key)
ciphertext: str = cipher.encrypt("my_text")
plaintext: str = cipher.decrypt(ciphertext)
assert plaintext == "my_text"
```

## FAQ or Troubleshooting

TODO: is it required? what do we need here?

If you encounter issues or have questions, please refer to our [FAQ](docs/faq.md) for solutions and guidance.

## Contributing

TODO: what are the conditions to contribute?

## About

Refers to pyproject.toml for information about:

- License
- Authors
- Maintainers
- References and Resources
    - Homepage
    - Documentation

## Changelog

TODO: is it required? what do we need here? 

See [CHANGELOG.md](CHANGELOG.md) for details about changes and updates in different versions of the library.

