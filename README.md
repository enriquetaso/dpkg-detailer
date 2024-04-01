# dpkg Detailer

API that exposes details about installed packages on Debian or Ubuntu systems through a JSON REST API.

## Setup

To run this API, you need to have Python 3.10+, Docker and Docker Compose installed.

Build the Docker app image and db:

```bash
make docker/build
```

Run the Docker container:

```bash
make docker/migrate

make docker/run
```

### Import packages:

 ```bash
 make docker/import_packages
 ```

Remove the Docker container:

```bash
make docker/stop
```

## Run tests:

```bash
make docker/tests
```

## Endpoints

### Get all packages:

```bash
GET http://0.0.0.0:8000/packages/
```

### Retrieve single package:

```bash
GET http://0.0.0.0:8000/packages/<package-name>/
```
