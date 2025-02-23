# competition-format-service

Backend service to administrate competition formats.

Supported [competition formats](https://assets.fis-ski.com/image/upload/v1624284540/fis-prod/assets/ICR_CrossCountry_2022_clean.pdf):

in this version:

- Interval Start competition,
- Individual sprint competition without a qualification round.

In future versions:

- Mass start competition,
- Skiathlon competition,
- Pursuit,
- Individual sprint competition with a qualification round,
- Team sprint competition, and
- Relay competitions.

## Usage example

```Shell
% curl -H "Content-Type: application/json" \
  -X POST \
  --data '{"username":"admin","password":"password"}' \
  http://localhost:8082/login
% export ACCESS="" #token from response
% curl -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS" \
  -X POST \
  --data @tests/files/competition_format_individual_sprint.json \
  http://localhost:8080/competition-formats
% curl http://localhost:8080/competition-formats # list all competition formats
% curl "http://localhost:8080/competition-formats?name=Individual%20Sprint" # search competition format by name
% curl http://localhost:8080/competition-formats/<the_id> # get competition format by id
% % curl \
  -H "Authorization: Bearer $ACCESS" \
  -X DELETE \
  http://localhost:8080/competition-formats/<the_id>
```

Look to the [openAPI specification](./specification.yaml) for the details.

## Running the API locally

Start the server locally:

```Shell
% uv run adev runserver -p 8080 --aux-port 8089 competition_format_service
```

## Running the API in a wsgi-server (gunicorn)

```Shell
% uv run gunicorn competition_format_service:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```

## Running the wsgi-server in Docker

To build and run the api in a Docker container:

```Shell
% docker build -t ghcr.io/langrenn-sprint/competition-format-service:latest .
% docker run --env-file .env -p 8080:8080 -d ghcr.io/langrenn-sprint/competition-format-service:latest
```

The easier way would be with docker compose:

```Shell
% docker compose up --build
```

## Running tests

We use [pytest](https://docs.pytest.org/en/latest/) for contract testing.

To run linters, checkers and tests:

```Shell
% uv run poe release
```

To run specific test:

```Shell
% uv run poe integration_test --no-cov -- tests/integration/test_competition_formats.py::test_create_competition_format_interval_start
```

To run tests with logging, do:

```Shell
% uv run poe integration_test  --log-cli-level=DEBUG
```

## Environment variables

An example .env file for local development:

```Shell
JWT_SECRET=secret
JWT_EXP_DELTA_SECONDS=3600
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
USERS_HOST_SERVER=localhost
USERS_HOST_PORT=8081
DB_USER=competition-format-service
DB_PASSWORD=password
LOGGING_LEVEL=DEBUG
```

## Clean __pycache__ files

```Shell
% py3clean .
```
