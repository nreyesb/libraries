# StorageUrl Verifier

This library aims to provide the verifier elements to use storage Url process.

## Works with

This requiries **python 3.11 or higher** and it's recommended to use [pyenv](https://github.com/pyenv/pyenv) for management python versions.

### As Library

Projects without poetry o for the local environment:

```bash
pip install toku-storage-url-verifier@{version}
```

Projects with poetry:

```bash
poetry add toku-storage-url-verifier@{version}
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
from toku.storage.url.core import UrlMetadata
from toku.storage.url.verifier import Verification

url_metadata: UrlMetadata = ...
verification: Verification = ...

verification.verify(url_metadata)
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
