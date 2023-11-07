# StorageUrl API

This library aims to provide the contract to use storage Url process.

## Works with

### As Library

Projects without poetry o for the local environment:

```bash
pip install toku-storage-url-api@{version}
```

Projects with poetry:

```bash
poetry add toku-storage-url-api@{version}
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
TODO
from toku.storage.url.api import StorageUrl  # not needed, just to show the type of class to use

with create_concrete_implementation() as storage_url:
    file = "data.text"
    content = "i'm the content"

    if not storage_url.exists(file)
        if storage_url.put_file_as(bytes(content, "utf-8"), file):
            content_1_: bytes = storage_url.get(file)

            with storage_url.get_as_input_stream(file) as input_stream:
                content_2: bytes = input_stream.read()
            
            print(content_1)
            print(content_2)
    
    files: list[str] = storage_url.files("")
    print(files)
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
- Maintainers
- References and Resources
    - Homepage
    - Documentation
