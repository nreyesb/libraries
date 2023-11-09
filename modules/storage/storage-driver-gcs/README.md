# StorageDriver GCS

This library aims to provide the implementation to use storage Driver GCS (Google Cloud Storage).

## Works with

### As Library

Projects without poetry o for the local environment:

```bash
pip install toku-storage-driver-gcs@{version}
```

Projects with poetry:

```bash
poetry add toku-storage-driver-gcs@{version}
```

The following command is useful to install the dependency in the poetry virtual environment for new version in progress, that means the library is not available in the remote repository for dowloanding but the code is available to build the dist or the dist is available in the local machine. It's important remember to run the command in the environment where the dependency is required and just add the dependency manually or change the version number in the pyproject.toml file, on that way it's not needed to use editable mode or path dependency in poetry:

```bash
poetry run python -m pip install {artifact_path}
```

#### Usage

##### Configuration

The library requires the followig configuration:

**Runtime**

- The GCP project needs to exists, the artifact doesn't create it.
- The bucket needs to exists, the artifact doesn't create it.
- The bucket has to be part of the same GCP project reported.
- The artifact requiries a JSON credentials file (a service account is recommended) with permissions over the bucket to perform read and write operations.

**Tests**

Set the following environment variables:

- GCP_PROJECT_ID = It's the id of the GCP project
- GCP_BUCKET_NAME = It's the name of the bucket
- GCP_CREDENTIALS_FILE = It's the JSON credentials file (a service account is recommended)

To do that it's possible to run `export {variable}={value}`

The tests will not create the bucket, but it considerers to delete the created
root folder for the tests to clean the bucket.

##### Example

To use the library, you can import it in your Python code:

```python
from toku.storage.driver.api import DirectorySeparator
from toku.storage.driver.gcs import GcsStorageDriver

with GcsStorageDriver(
    root="my_folder",
    project_id="project_id_as79",
    bucket_name="bucket_name_asd7",
    credentials_file="/c/user/home/sa_account.json"
) as storage_driver:
    file = "data.txt"
    content = "i'm the content"

    if not storage_driver.exists(file)
        if storage_driver.put_file_as(bytes(content, "utf-8"), file):
            content_1_: bytes = storage_driver.get(file)

            with storage_driver.get_as_input_stream(file) as input_stream:
                content_2: bytes = input_stream.read()
            
            print(content_1)
            print(content_2)
    
    files: list[str] = storage_driver.files("")
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

poetry run pytest -n {WORKERS} -v --cov --cov-fail-under={MIN}
```

## About

Refers to **pyproject.toml** for information about:

- License
- Authors
- References and Resources
    - Homepage
    - Documentation
