# StorageUrl Core

This library aims to provide the core elements to use storage Url process.

## Works with

This requiries **python 3.11 or higher** and it's recommended to use [pyenv](https://github.com/pyenv/pyenv) for management python versions.

### As Library

Projects without poetry o for the local environment:

```bash
pip install toku-storage-url-core@{version}
```

Projects with poetry:

```bash
poetry add toku-storage-url-core@{version}
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
# UrlEncode
from toku.storage.url.core import UrlEncode
from toku.storage.url.core import UrlSchema

url_encoded = UrlEncoded(
    UrlSchema.HTTPS,
    "www.my-domain.com",
    "storage/url/streaming/{metadata}",
    "a9s087dygsabkhjy0d8as798f7ti6asthgfcv"
)
print(url_encoded)
```

```python
# UrlMetadata minimum arguments
from datetime import timedelta
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import DateTime

access_from: DateTime = DateTime.create()
access_until: DateTime = DateTime.create(access_from.get()).delta(timedelta(hours=2, days=4))

url_metadata: UrlMetadata = UrlMetadata \
    .builder(
        path="directory/file.txt",
        storage_driver_reference="sd_reference"
    ) \
    .build()
print(url_metadata)
```

```python
# UrlMetadata full arguments
from datetime import timedelta
from toku.storage.url.core import UrlMetadata
from toku.storage.url.core import Classification
from toku.storage.url.core import Principal
from toku.storage.url.core import Condition
from toku.storage.url.core import DateTimeCondition
from toku.storage.url.core import DateTime

access_from: DateTime = DateTime.create()
access_until: DateTime = DateTime.create(access_from.get()).delta(timedelta(hours=2, days=4))

url_metadata: UrlMetadata = UrlMetadata \
    .builder(
        path="directory/file.txt",
        storage_driver_reference="sd_reference"
    ) \
    .classification(Classification.CONFIDENTIAL) \
    .principal(Principal("USER")) \
    .condition(Condition(
        DateTimeCondition(
            access_from=access_from.to_millis(),
            access_until=access_until.to_millis()
        )
    )) \
    .metadata({
        "key1": "value1",
        "key2": "value2"
    }) \
    .build()
print(url_metadata)
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

poetry run pytest -n 2 -v --cov --cov-fail-under=MIN
```

## About

Refers to **pyproject.toml** for information about:

- License
- Authors
- References and Resources
    - Homepage
    - Documentation
