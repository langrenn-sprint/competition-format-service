"""Integration test cases for the competition_formats route."""

import os
import uuid
from copy import deepcopy
from http import HTTPStatus
from typing import Any

import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import TypeAdapter
from pytest_mock import MockFixture

from app import api
from app.models import CompetitionFormatUnion

USERS_HOST_SERVER = os.getenv("USERS_HOST_SERVER")
USERS_HOST_PORT = os.getenv("USERS_HOST_PORT")


@pytest.fixture
def client() -> TestClient:
    """Fixture to create a test client for the FastAPI application."""
    return TestClient(api)


@pytest.fixture
def token() -> str:
    """Create a valid token."""
    secret = os.getenv("JWT_SECRET")
    algorithm = "HS256"
    payload = {
        "username": os.getenv("ADMIN_USERNAME"),
        "role": "admin",
        "exp": 9999999999,
    }
    return jwt.encode(payload, secret, algorithm)


@pytest.fixture
def token_unsufficient_role() -> str:
    """Create a valid token."""
    secret = os.getenv("JWT_SECRET")
    algorithm = "HS256"
    payload = {"username": "user", "role": "event-admin", "exp": 9999999999}
    return jwt.encode(payload, secret, algorithm)


@pytest.fixture
async def competition_format_interval_start() -> dict[str, int | str]:
    """An competition_format object for testing."""
    return {
        "datatype": "interval_start",
        "id": "290e70d5-0933-4af0-bb53-1d705ba7eb95",
        "name": "Interval Start",
        "starting_order": "Draw",
        "start_procedure": "Interval Start",
        "time_between_groups": "00:10:00",
        "intervals": "00:00:30",
        "max_no_of_contestants_in_raceclass": 9999,
        "max_no_of_contestants_in_race": 9999,
    }


@pytest.fixture
async def competition_format_individual_sprint() -> dict[str, Any]:
    """An competition_format object for testing."""
    return {
        "datatype": "individual_sprint",
        "id": "290e70d5-0933-4af0-bb53-1d705ba7eb95",
        "name": "Individual Sprint",
        "starting_order": "Draw",
        "start_procedure": "Heat Start",
        "time_between_groups": "00:10:00",
        "time_between_rounds": "00:05:00",
        "time_between_heats": "00:02:30",
        "max_no_of_contestants_in_raceclass": 80,
        "max_no_of_contestants_in_race": 10,
        "rounds_ranked_classes": ["Q", "S", "F"],
        "rounds_non_ranked_classes": ["R1", "R2"],
        "race_config_non_ranked": [
            {
                "max_no_of_contestants": 7,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 1},
                    "R2": {"A": 1},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 16,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 2},
                    "R2": {"A": 2},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 24,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 3},
                    "R2": {"A": 3},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 32,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 4},
                    "R2": {"A": 4},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 40,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 6},
                    "R2": {"A": 6},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 48,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 6},
                    "R2": {"A": 6},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 56,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 7},
                    "R2": {"A": 7},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
            {
                "max_no_of_contestants": 80,
                "rounds": ["R1", "R2"],
                "no_of_heats": {
                    "R1": {"A": 8},
                    "R2": {"A": 8},
                },
                "from_to": {
                    "R1": {"A": {"R2": {"A": "ALL"}}},
                },
            },
        ],
        "race_config_ranked": [
            {
                "max_no_of_contestants": 7,
                "rounds": ["Q", "F"],
                "no_of_heats": {
                    "Q": {"A": 1},
                    "F": {"A": 1, "B": 0, "C": 0},
                },
                "from_to": {
                    "Q": {"A": {"F": {"A": "ALL", "B": 0}}, "C": {"F": {"C": 0}}},
                },
            },
            {
                "max_no_of_contestants": 16,
                "rounds": ["Q", "F"],
                "no_of_heats": {
                    "Q": {"A": 2},
                    "F": {"A": 1, "B": 1, "C": 0},
                },
                "from_to": {
                    "Q": {"A": {"F": {"A": 4, "B": "REST"}}, "C": {"F": {"C": 0}}},
                },
            },
            {
                "max_no_of_contestants": 24,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 3},
                    "S": {"A": 2, "C": 0},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 5, "C": 0}, "F": {"C": "REST"}}},
                    "S": {"A": {"F": {"A": 4, "B": "REST"}}, "C": {"F": {"C": 0}}},
                },
            },
            {
                "max_no_of_contestants": 32,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 4},
                    "S": {"A": 2, "C": 2},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 4, "C": "REST"}}},
                    "S": {"A": {"F": {"A": 4, "B": "REST"}}, "C": {"F": {"C": 4}}},
                },
            },
            {
                "max_no_of_contestants": 40,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 6},
                    "S": {"A": 4, "C": 2},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 4, "C": "REST"}}},
                    "S": {"A": {"F": {"A": 2, "B": 2}}, "C": {"F": {"C": 4}}},
                },
            },
            {
                "max_no_of_contestants": 48,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 6},
                    "S": {"A": 4, "C": 4},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 4, "C": "REST"}}},
                    "S": {"A": {"F": {"A": 2, "B": 2}}, "C": {"F": {"C": 2}}},
                },
            },
            {
                "max_no_of_contestants": 56,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 7},
                    "S": {"A": 4, "C": 4},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 4, "C": "REST"}}},
                    "S": {"A": {"F": {"A": 2, "B": 2}}, "C": {"F": {"C": 2}}},
                },
            },
            {
                "max_no_of_contestants": 80,
                "rounds": ["Q", "S", "F"],
                "no_of_heats": {
                    "Q": {"A": 8},
                    "S": {"A": 4, "C": 4},
                    "F": {"A": 1, "B": 1, "C": 1},
                },
                "from_to": {
                    "Q": {"A": {"S": {"A": 4, "C": "REST"}}},
                    "S": {"A": {"F": {"A": 2, "B": 2}}, "C": {"F": {"C": 2}}},
                },
            },
        ],
    }


@pytest.mark.integration
async def test_create_competition_format_interval_start(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return Created, location header."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    request_body = competition_format_interval_start

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.CREATED
    assert (
        f"/competition-formats/{competition_format_interval_start['id']}"
        in resp.headers["Location"]
    )


@pytest.mark.integration
async def test_create_competition_format_individual_sprint(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return Created, location header."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    request_body = competition_format_individual_sprint

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.CREATED
    assert (
        f"/competition-formats/{competition_format_individual_sprint['id']}"
        in resp.headers["Location"]
    )


@pytest.mark.integration
async def test_get_competition_format_interval_start_by_id(
    client: TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=competition_format_interval_start,
    )

    resp = client.get(f"/competition-formats/{competition_format_id}")
    assert resp.status_code == HTTPStatus.OK
    assert "application/json" in resp.headers["Content-Type"]
    body = resp.json()
    assert type(body) is dict
    assert body["id"] == competition_format_id
    assert body["datatype"] == competition_format_interval_start["datatype"]
    assert body["name"] == competition_format_interval_start["name"]
    assert body["starting_order"] == competition_format_interval_start["starting_order"]
    assert (
        body["start_procedure"] == competition_format_interval_start["start_procedure"]
    )
    assert (
        body["time_between_groups"]
        == competition_format_interval_start["time_between_groups"]
    )
    assert body["intervals"] == competition_format_interval_start["intervals"]
    assert (
        body["max_no_of_contestants_in_raceclass"]
        == competition_format_interval_start["max_no_of_contestants_in_raceclass"]
    )
    assert (
        body["max_no_of_contestants_in_race"]
        == competition_format_interval_start["max_no_of_contestants_in_race"]
    )


@pytest.mark.integration
async def test_get_competition_format_individual_sprint_by_id(
    client: TestClient,
    mocker: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id}
        | competition_format_individual_sprint,
    )

    resp = client.get(f"/competition-formats/{competition_format_id}")
    assert resp.status_code == HTTPStatus.OK
    assert "application/json" in resp.headers["Content-Type"]
    body = resp.json()
    assert type(body) is dict
    assert body["datatype"] == competition_format_individual_sprint["datatype"]
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
        body["time_between_groups"]
        == competition_format_individual_sprint["time_between_groups"]
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
    assert (
        body["rounds_ranked_classes"]
        == competition_format_individual_sprint["rounds_ranked_classes"]
    )
    assert (
        body["rounds_non_ranked_classes"]
        == competition_format_individual_sprint["rounds_non_ranked_classes"]
    )


@pytest.mark.integration
async def test_get_competition_formats_by_name(
    client: TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    competition_format_name = competition_format_interval_start["name"]
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )

    resp = client.get(f"/competition-formats?name={competition_format_name}")
    assert resp.status_code == HTTPStatus.OK
    assert "application/json" in resp.headers["Content-Type"]
    body = resp.json()
    assert type(body) is list
    assert body[0]["id"] == competition_format_id
    assert body[0]["name"] == competition_format_interval_start["name"]
    assert (
        body[0]["starting_order"] == competition_format_interval_start["starting_order"]
    )
    assert (
        body[0]["start_procedure"]
        == competition_format_interval_start["start_procedure"]
    )
    assert body[0]["intervals"] == competition_format_interval_start["intervals"]


@pytest.mark.integration
async def test_get_competition_formats_by_name_individual_sprint(
    client: TestClient,
    mocker: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    competition_format_name = competition_format_individual_sprint["name"]
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_individual_sprint
        ],
    )

    resp = client.get(f"/competition-formats?name={competition_format_name}")
    assert resp.status_code == HTTPStatus.OK
    assert "application/json" in resp.headers["Content-Type"]
    body = resp.json()
    assert type(body) is list
    assert body[0]["id"] == competition_format_id
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


@pytest.mark.integration
async def test_update_competition_format_interval_start(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    new_name = "Oslo Skagen competition-format"
    request_body = deepcopy(competition_format_interval_start)
    request_body["id"] = competition_format_id
    request_body["name"] = new_name

    resp = client.put(
        f"/competition-formats/{competition_format_id}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.integration
async def test_update_competition_format_individual_sprint(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_individual_sprint
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    new_name = "Oslo Skagen competition-format"
    request_body = deepcopy(competition_format_individual_sprint)
    request_body["id"] = competition_format_id
    request_body["name"] = new_name

    resp = client.put(
        f"/competition-formats/{competition_format_id}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.integration
async def test_get_all_competition_formats(
    client: TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK and a valid json body."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_all_competition_formats",
        return_value=[
            TypeAdapter(CompetitionFormatUnion).validate_python(
                competition_format_interval_start
            ),
            TypeAdapter(CompetitionFormatUnion).validate_python(
                competition_format_individual_sprint
            ),
        ],
    )

    resp = client.get("/competition-formats")
    assert resp.status_code == HTTPStatus.OK
    assert "application/json" in resp.headers["Content-Type"]
    body = resp.json()
    assert type(body) is list
    assert len(body) > 0
    assert body[0]["id"] == competition_format_id


@pytest.mark.integration
async def test_delete_competition_format_by_id(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=competition_format_id,
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }

    resp = client.delete(
        f"/competition-formats/{competition_format_id}", headers=headers
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT


# Bad cases


@pytest.mark.integration
async def test_create_competition_format_interval_start_unknown_datatype(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 UNPROCESSABLE ENTITY."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = deepcopy(competition_format_interval_start)
    request_body["datatype"] = "unknown"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_interval_start_already_exist(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 400 Bad request entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[{id: competition_format_id} | competition_format_interval_start],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = competition_format_interval_start

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


# Mandatory properties missing at create and update:
@pytest.mark.integration
async def test_create_competition_format_missing_mandatory_property(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = {"optional_property": "Optional_property"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_with_input_id(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 201 Created."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = competition_format_interval_start
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.CREATED
    assert f"/competition-formats/{competition_format_id}" in resp.headers["Location"]


@pytest.mark.integration
async def test_create_competition_format_adapter_fails(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 400 HTTPBadRequest."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=None,
    )
    request_body = competition_format_interval_start
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.integration
async def test_update_competition_format_unknown_datatype(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 UNPROCESSABLE ENTITY."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_body = deepcopy(competition_format_interval_start)
    request_body["datatype"] = "unknown"

    resp = client.put(
        f"/competition-formats/{competition_format_interval_start['id']}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_update_competition_format_by_id_missing_mandatory_property(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_body = {
        "id": competition_format_interval_start["id"],
        "optional_property": "Optional_property",
    }

    resp = client.put(
        f"/competition-formats/{competition_format_interval_start['id']}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_update_competition_format_by_id_different_id_in_body(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    competition_format_id = competition_format_interval_start["id"]
    competition_format_interval_start["id"] = uuid.uuid4().hex

    resp = client.put(
        f"/competition-formats/{competition_format_id}",
        headers=headers,
        json=competition_format_interval_start,
    )

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_intervals(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    competition_format_with_invalid_intervals = deepcopy(
        competition_format_interval_start
    )
    competition_format_with_invalid_intervals["intervals"] = "99:99:99"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_with_invalid_intervals,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_groups(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_with_invalid_time_between_groups = deepcopy(
        competition_format_interval_start
    )
    competition_format_with_invalid_time_between_groups["time_between_groups"] = (
        "99:99:99"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_with_invalid_time_between_groups,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_rounds(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_with_invalid_time_between_rounds = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_with_invalid_time_between_rounds["time_between_rounds"] = (
        "99:99:99"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_with_invalid_time_between_rounds,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_heats(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_with_invalid_time_between_heats = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_with_invalid_time_between_heats["time_between_heats"] = (
        "00:00:00"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_with_invalid_time_between_heats,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_race_config_non_ranked(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["race_config_non_ranked"] = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_without_race_config,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_race_config_ranked(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["race_config_ranked"] = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_without_race_config,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_rounds_non_ranked_classes(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["rounds_non_ranked_classes"] = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_without_race_config,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_rounds_ranked_classes(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_individual_sprint["id"],
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["rounds_ranked_classes"] = []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = client.post(
        "/competition-formats",
        headers=headers,
        json=competition_format_without_race_config,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_update_competition_format_invalid_interval(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    updated_competition_format = deepcopy(competition_format_interval_start)
    updated_competition_format["id"] = competition_format_interval_start["id"]
    updated_competition_format["intervals"] = "99:99:99"

    resp = client.put(
        f"/competition-formats/{competition_format_interval_start['id']}",
        headers=headers,
        json=updated_competition_format,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Unauthorized cases:


@pytest.mark.integration
async def test_create_competition_format_no_authorization(
    client: TestClient, mocker: MockFixture, competition_format_interval_start: dict
) -> None:
    """Should return 401 Unauthorized."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    request_body = competition_format_interval_start
    headers = {
        "Content-Type": "application/json",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
async def test_update_competition_format_by_id_no_authorization(
    client: TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 401 Unauthorized."""
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_interval_start["id"],
    )

    headers = {
        "Content-Type": "application/json",
    }

    request_body = competition_format_interval_start

    resp = client.put(
        f"/competition-formats/{competition_format_interval_start['id']}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED, resp.text


@pytest.mark.integration
async def test_delete_competition_format_by_id_no_authorization(
    client: TestClient, mocker: MockFixture, competition_format_interval_start: dict
) -> None:
    """Should return 401 Unauthorized."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=TypeAdapter(CompetitionFormatUnion).validate_python(
            competition_format_interval_start
        ),
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=competition_format_id,
    )

    resp = client.delete(f"/competition-formats/{competition_format_id}")
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


# Forbidden:
@pytest.mark.integration
async def test_create_competition_format_insufficient_role(
    client: TestClient,
    mocker: MockFixture,
    token_unsufficient_role: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 403 Forbidden."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = competition_format_interval_start
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_unsufficient_role}",
    }

    resp = client.post("/competition-formats", headers=headers, json=request_body)
    assert resp.status_code == HTTPStatus.FORBIDDEN, resp.text


# NOT FOUND CASES:


@pytest.mark.integration
async def test_get_competition_format_not_found(
    client: TestClient,
    mocker: MockFixture,
) -> None:
    """Should return 404 Not found."""
    competition_format_id = uuid.uuid4().hex
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )

    resp = client.get(f"/competition-formats/{competition_format_id}")
    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.integration
async def test_get_competition_formats_by_name_not_found(
    client: TestClient, mocker: MockFixture
) -> None:
    """Should return 200 OK and empty list."""
    competition_format_name = "does-not-exist"
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )

    resp = client.get(f"/competition-formats?name={competition_format_name}")
    assert resp.status_code == HTTPStatus.OK
    body = resp.json()
    assert type(body) is list
    assert len(body) == 0


@pytest.mark.integration
async def test_update_competition_format_not_found(
    client: TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 404 Not found."""
    competition_format_id = uuid.uuid4().hex
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=None,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_body = competition_format_interval_start

    resp = client.put(
        f"/competition-formats/{competition_format_id}",
        headers=headers,
        json=request_body,
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.integration
async def test_delete_competition_format_not_found(
    client: TestClient, mocker: MockFixture, token: MockFixture
) -> None:
    """Should return 404 Not found."""
    competition_format_id = uuid.uuid4().hex
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )
    mocker.patch(
        "app.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=None,
    )

    headers = {
        "Authorization": f"Bearer {token}",
    }

    resp = client.delete(
        f"/competition-formats/{competition_format_id}", headers=headers
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND
