"""Contract test cases for competition-formats."""

import logging
import os
from collections.abc import AsyncGenerator
from copy import deepcopy
from http import HTTPStatus
from json import load
from pathlib import Path
from typing import Any
from urllib.parse import quote

import motor.motor_asyncio
import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

USERS_HOST_SERVER = os.getenv("USERS_HOST_SERVER")
USERS_HOST_PORT = os.getenv("USERS_HOST_PORT")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "27017"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
async def token(http_service: Any) -> str:
    """Create a valid token."""
    url = f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/login"
    headers = {"Content-Type": "application/json"}
    request_body = {
        "username": os.getenv("ADMIN_USERNAME"),
        "password": os.getenv("ADMIN_PASSWORD"),
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        body = response.json()
    if response.status_code != HTTPStatus.OK:
        logger.error(
            f"Got unexpected status {response.status_code} from {http_service}."
        )
    return body["token"]


@pytest.fixture(scope="module", autouse=True)
async def clear_db() -> AsyncGenerator:
    """Clear db before and after tests."""
    logger.info(" --- Cleaning db at startup. ---")
    mongo = motor.motor_asyncio.AsyncIOMotorClient(
        host=DB_HOST, port=DB_PORT, username=DB_USER, password=DB_PASSWORD
    )
    try:
        await mongo.drop_database(f"{DB_NAME}")
    except Exception as error:
        logger.exception(f"Failed to drop database {DB_NAME}.")
        raise error from None
    logger.info(" --- Testing starts. ---")

    yield

    logger.info(" --- Testing finished. ---")
    logger.info(" --- Cleaning db after testing. ---")
    try:
        await mongo.drop_database(f"{DB_NAME}")
    except Exception as error:
        logger.exception(f"Failed to drop database {DB_NAME}.")
        raise error from None
    logger.info(" --- Cleaning db done. ---")


@pytest.fixture(scope="module")
async def competition_format_interval_start() -> dict:
    """An competition_format object for testing."""
    with open("tests/files/competition_format_interval_start.json") as file:
        return load(file)


@pytest.fixture(scope="module")
async def competition_format_individual_sprint() -> dict:
    """An competition_format object for testing."""
    with open("tests/files/competition_format_individual_sprint.json") as file:
        return load(file)


@pytest.mark.contract
@pytest.mark.anyio
async def test_create_competition_format_interval_start(
    http_service: Any,
    token: MockFixture,
    clear_db: AsyncGenerator,
    competition_format_interval_start: dict,
) -> None:
    """Should return Created, location header and no body."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_body = competition_format_interval_start

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        status = response.status_code
        body = response.json() if response.content else None

    assert status == HTTPStatus.CREATED, f"body:{body}" if body else ""
    assert "/competition-formats/" in response.headers["Location"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_competition_format_individual_sprint(
    http_service: Any,
    token: MockFixture,
    clear_db: AsyncGenerator,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return Created, location header and no body."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_body = competition_format_individual_sprint

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        status = response.status_code
        body = response.json() if response.content else None

    assert status == HTTPStatus.CREATED, f"body:{body}" if body else ""
    assert "/competition-formats/" in response.headers["Location"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_competition_format_individual_sprint_multiple_finals_1(
    http_service: Any,
    token: MockFixture,
    clear_db: AsyncGenerator,
) -> None:
    """Should return Created, location header and no body."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    with Path(
        "tests/files/competition_format_individual_sprint_multiple_finals_1.json"
    ).open("r") as file:
        competition_format = load(file)

    request_body = competition_format

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        status = response.status_code
        body = response.json() if response.content else None

    assert status == HTTPStatus.CREATED, f"body:{body}" if body else ""
    assert "/competition-formats/" in response.headers["Location"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_create_competition_format_individual_sprint_multiple_finals_2(
    http_service: Any,
    token: MockFixture,
    clear_db: AsyncGenerator,
) -> None:
    """Should return Created, location header and no body."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    with open(
        "tests/files/competition_format_individual_sprint_multiple_finals_2.json"
    ) as file:
        competition_format = load(file)

    request_body = competition_format

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        status = response.status_code
        body = response.json() if response.content else None

    assert status == HTTPStatus.CREATED, f"body:{body}" if body else ""
    assert "/competition-formats/" in response.headers["Location"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_all_competition_formats(
    http_service: Any,
) -> None:
    """Should return OK and a list of competition_formats as json."""
    url = f"{http_service}/competition-formats"

    async with AsyncClient() as client:
        response = await client.get(url)
        competition_formats = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "application/json" in response.headers["Content-Type"]
    assert type(competition_formats) is list
    assert len(competition_formats) > 0


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_competition_format_by_id(
    http_service: Any, competition_format_individual_sprint: dict
) -> None:
    """Should return OK and an competition_format as json."""
    url = f"{http_service}/competition-formats"

    async with AsyncClient() as client:
        query_param = f"name={quote(competition_format_individual_sprint['name'])}"
        response = await client.get(f"{url}?{query_param}")
        competition_formats = response.json()
        competition_format_id = competition_formats[0]["id"]
        url = f"{url}/{competition_format_id}"
        response = await client.get(url)
        body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "application/json" in response.headers["Content-Type"]
    assert type(competition_format_individual_sprint) is dict
    assert body["id"] == competition_format_id
    assert body["name"] == competition_format_individual_sprint["name"]
    assert (
        body["starting_order"] == competition_format_individual_sprint["starting_order"]
    )
    assert (
        body["start_procedure"]
        == competition_format_individual_sprint["start_procedure"]
    )
    assert (
        body["time_between_rounds"]
        == competition_format_individual_sprint["time_between_rounds"]
    )
    assert (
        body["time_between_heats"]
        == competition_format_individual_sprint["time_between_heats"]
    )
    assert (
        body["max_no_of_contestants_in_raceclass"]
        == competition_format_individual_sprint["max_no_of_contestants_in_raceclass"]
    )
    assert (
        body["max_no_of_contestants_in_race"]
        == competition_format_individual_sprint["max_no_of_contestants_in_race"]
    )
    # Check that the race_config_non_ranked is sorted on max_no_of_contestants:
    assert all(
        body["race_config_non_ranked"][i]["max_no_of_contestants"]
        <= body["race_config_non_ranked"][i + 1]["max_no_of_contestants"]
        for i in range(len(body["race_config_non_ranked"]) - 1)
    )
    # Check that the race_config_ranked is sorted on max_no_of_contestants:
    assert all(
        body["race_config_ranked"][i]["max_no_of_contestants"]
        <= body["race_config_ranked"][i + 1]["max_no_of_contestants"]
        for i in range(len(body["race_config_ranked"]) - 1)
    )

    competition_format_individual_sprint["race_config_ranked"].sort(
        key=lambda x: x["max_no_of_contestants"]
    )
    assert (
        body["race_config_ranked"]
        == competition_format_individual_sprint["race_config_ranked"]
    )
    competition_format_individual_sprint["race_config_non_ranked"].sort(
        key=lambda x: x["max_no_of_contestants"]
    )
    assert (
        body["race_config_non_ranked"]
        == competition_format_individual_sprint["race_config_non_ranked"]
    )


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_competition_format_by_name_interval_start(
    http_service: Any, competition_format_interval_start: dict
) -> None:
    """Should return OK and an competition_format as json."""
    url = f"{http_service}/competition-formats"

    async with AsyncClient() as client:
        query_param = f"name={quote(competition_format_interval_start['name'])}"
        response = await client.get(f"{url}?{query_param}")

        assert str(response.url) == f"{url}?name=Interval%20Start"
        body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "application/json" in response.headers["Content-Type"]
    assert type(body) is list
    assert len(body) == 1
    assert body[0]["id"]
    assert body[0]["name"] == competition_format_interval_start["name"]
    assert (
        body[0]["starting_order"] == competition_format_interval_start["starting_order"]
    )
    assert (
        body[0]["start_procedure"]
        == competition_format_interval_start["start_procedure"]
    )


@pytest.mark.contract
@pytest.mark.asyncio
async def test_get_competition_format_by_name_individual_sprint(
    http_service: Any, competition_format_individual_sprint: dict
) -> None:
    """Should return OK and an competition_format as json."""
    url = f"{http_service}/competition-formats"

    async with AsyncClient() as client:
        query_param = f"name={quote(competition_format_individual_sprint['name'])}"
        response = await client.get(f"{url}?{query_param}")

        assert str(response.url) == f"{url}?name=Individual%20Sprint"
        body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "application/json" in response.headers["Content-Type"]
    assert type(competition_format_individual_sprint) is dict
    assert body[0]["id"]
    assert body[0]["name"] == competition_format_individual_sprint["name"]
    assert (
        body[0]["starting_order"]
        == competition_format_individual_sprint["starting_order"]
    )
    assert (
        body[0]["start_procedure"]
        == competition_format_individual_sprint["start_procedure"]
    )
    assert (
        body[0]["time_between_rounds"]
        == competition_format_individual_sprint["time_between_rounds"]
    )
    assert (
        body[0]["time_between_heats"]
        == competition_format_individual_sprint["time_between_heats"]
    )
    assert (
        body[0]["max_no_of_contestants_in_raceclass"]
        == competition_format_individual_sprint["max_no_of_contestants_in_raceclass"]
    )
    assert (
        body[0]["max_no_of_contestants_in_race"]
        == competition_format_individual_sprint["max_no_of_contestants_in_race"]
    )
    # Check that the race_config_non_ranked is sorted on max_no_of_contestants:
    assert all(
        body[0]["race_config_non_ranked"][i]["max_no_of_contestants"]
        <= body[0]["race_config_non_ranked"][i + 1]["max_no_of_contestants"]
        for i in range(len(body[0]["race_config_non_ranked"]) - 1)
    )
    # Check that the race_config_ranked is sorted on max_no_of_contestants:
    assert all(
        body[0]["race_config_ranked"][i]["max_no_of_contestants"]
        <= body[0]["race_config_ranked"][i + 1]["max_no_of_contestants"]
        for i in range(len(body[0]["race_config_ranked"]) - 1)
    )

    competition_format_individual_sprint["race_config_ranked"].sort(
        key=lambda x: x["max_no_of_contestants"]
    )
    assert (
        body[0]["race_config_ranked"]
        == competition_format_individual_sprint["race_config_ranked"]
    )
    competition_format_individual_sprint["race_config_non_ranked"].sort(
        key=lambda x: x["max_no_of_contestants"]
    )
    assert (
        body[0]["race_config_non_ranked"]
        == competition_format_individual_sprint["race_config_non_ranked"]
    )


@pytest.mark.contract
@pytest.mark.asyncio
async def test_update_competition_format_interval_start(
    http_service: Any, token: MockFixture, competition_format_interval_start: dict
) -> None:
    """Should return No Content."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    async with AsyncClient() as client:
        response = await client.get(url)
        competition_formats = response.json()
        competition_format_id = competition_formats[0]["id"]
        url = f"{url}/{competition_format_id}"

        request_body = deepcopy(competition_format_interval_start)
        new_name = "Interval Start updated"
        request_body["id"] = competition_format_id
        request_body["name"] = new_name

        response = await client.put(url, headers=headers, json=request_body)
        assert response.status_code == HTTPStatus.NO_CONTENT

        response = await client.get(url)
        assert response.status_code == HTTPStatus.OK
        updated_competition_format = response.json()

    assert updated_competition_format["name"] == new_name


@pytest.mark.contract
@pytest.mark.asyncio
async def test_update_competition_format_individual_sprint(
    http_service: Any, token: MockFixture, competition_format_individual_sprint: dict
) -> None:
    """Should return No Content."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    async with AsyncClient() as client:
        response = await client.get(url)
        competition_formats = response.json()
        competition_format_id = competition_formats[0]["id"]
        url = f"{url}/{competition_format_id}"

        request_body = deepcopy(competition_format_individual_sprint)
        new_name = "Individual Sprint updated"
        request_body["id"] = competition_format_id
        request_body["name"] = new_name
        request_body["race_config_non_ranked"].append(
            {
                "max_no_of_contestants": 4,
                "rounds": ["R1", "R2"],
                "no_of_heats": {"R1": {"A": 1}, "R2": {"A": 1}},
                "from_to": {"R1": {"A": {"R2": {"A": "ALL"}}}},
            },
        )

        response = await client.put(url, headers=headers, json=request_body)
        assert response.status_code == HTTPStatus.NO_CONTENT

        response = await client.get(url)
        assert response.status_code == HTTPStatus.OK
        updated_competition_format = response.json()

    assert updated_competition_format["name"] == new_name

    # Check that the race_config_non_ranked is sorted on max_no_of_contestants:
    assert all(
        updated_competition_format["race_config_non_ranked"][i]["max_no_of_contestants"]
        <= updated_competition_format["race_config_non_ranked"][i + 1][
            "max_no_of_contestants"
        ]
        for i in range(len(updated_competition_format["race_config_non_ranked"]) - 1)
    )
    # Check that the race_config_ranked is sorted on max_no_of_contestants:
    assert all(
        updated_competition_format["race_config_ranked"][i]["max_no_of_contestants"]
        <= updated_competition_format["race_config_ranked"][i + 1][
            "max_no_of_contestants"
        ]
        for i in range(len(updated_competition_format["race_config_ranked"]) - 1)
    )


@pytest.mark.contract
@pytest.mark.asyncio
async def test_delete_competition_format(http_service: Any, token: MockFixture) -> None:
    """Should return No Content."""
    url = f"{http_service}/competition-formats"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    async with AsyncClient() as client:
        response = await client.get(url)
        competition_formats = response.json()
        competition_format_id = competition_formats[0]["id"]
        url = f"{url}/{competition_format_id}"
        response = await client.delete(url, headers=headers)
        assert response.status_code == HTTPStatus.NO_CONTENT

        response = await client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
