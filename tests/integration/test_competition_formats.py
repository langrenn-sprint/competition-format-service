"""Integration test cases for the competition_formats route."""

import os
from copy import deepcopy
from http import HTTPStatus
from typing import Any

import jwt
import pytest
from aiohttp import hdrs
from aiohttp.test_utils import TestClient as _TestClient
from aioresponses import aioresponses
from multidict import MultiDict
from pytest_mock import MockFixture

USERS_HOST_SERVER = os.getenv("USERS_HOST_SERVER")
USERS_HOST_PORT = os.getenv("USERS_HOST_PORT")


@pytest.fixture
def token() -> str:
    """Create a valid token."""
    secret = os.getenv("JWT_SECRET")
    algorithm = "HS256"
    payload = {"identity": os.getenv("ADMIN_USERNAME"), "roles": ["admin"]}
    return jwt.encode(payload, secret, algorithm)


@pytest.fixture
def token_unsufficient_role() -> str:
    """Create a valid token."""
    secret = os.getenv("JWT_SECRET")
    algorithm = "HS256"
    payload = {"identity": "user", "roles": ["event-admin"]}
    return jwt.encode(payload, secret, algorithm)


@pytest.fixture
async def competition_format_interval_start() -> dict[str, int | str]:
    """An competition_format object for testing."""
    return {
        "name": "Interval Start",
        "starting_order": "Draw",
        "start_procedure": "Interval Start",
        "time_between_groups": "00:10:00",
        "intervals": "00:00:30",
        "max_no_of_contestants_in_raceclass": 9999,
        "max_no_of_contestants_in_race": 9999,
        "datatype": "interval_start",
    }


@pytest.fixture
async def competition_format_individual_sprint() -> dict[str, Any]:
    """An competition_format object for testing."""
    return {
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
        "datatype": "individual_sprint",
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
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return Created, location header."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = competition_format_interval_start

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.CREATED
        assert (
            f"/competition-formats/{competition_format_id}"
            in resp.headers[hdrs.LOCATION]
        )


@pytest.mark.integration
async def test_create_competition_format_individual_sprint(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return Created, location header."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = competition_format_individual_sprint

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.CREATED
        assert (
            f"/competition-formats/{competition_format_id}"
            in resp.headers[hdrs.LOCATION]
        )


@pytest.mark.integration
async def test_get_competition_format_interval_start_by_id(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats/{competition_format_id}")
        assert resp.status == HTTPStatus.OK
        assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]
        body = await resp.json()
        assert type(body) is dict
        assert body["id"] == competition_format_id
        assert body["name"] == competition_format_interval_start["name"]
        assert (
            body["starting_order"]
            == competition_format_interval_start["starting_order"]
        )
        assert (
            body["start_procedure"]
            == competition_format_interval_start["start_procedure"]
        )
        assert body["intervals"] == competition_format_interval_start["intervals"]


@pytest.mark.integration
async def test_get_competition_format_individual_sprint_by_id(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id}
        | competition_format_individual_sprint,
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats/{competition_format_id}")
        assert resp.status == HTTPStatus.OK
        assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]
        body = await resp.json()
        assert type(body) is dict
        assert body["id"] == competition_format_id
        assert body["name"] == competition_format_individual_sprint["name"]
        assert (
            body["starting_order"]
            == competition_format_individual_sprint["starting_order"]
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
            == competition_format_individual_sprint[
                "max_no_of_contestants_in_raceclass"
            ]
        )
        assert (
            body["max_no_of_contestants_in_race"]
            == competition_format_individual_sprint["max_no_of_contestants_in_race"]
        )


@pytest.mark.integration
async def test_get_competition_formats_by_name(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    competition_format_name = competition_format_interval_start["name"]
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats?name={competition_format_name}")
        assert resp.status == HTTPStatus.OK
        assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]
        body = await resp.json()
        assert type(body) is list
        assert body[0]["id"] == competition_format_id
        assert body[0]["name"] == competition_format_interval_start["name"]
        assert (
            body[0]["starting_order"]
            == competition_format_interval_start["starting_order"]
        )
        assert (
            body[0]["start_procedure"]
            == competition_format_interval_start["start_procedure"]
        )
        assert body[0]["intervals"] == competition_format_interval_start["intervals"]


@pytest.mark.integration
async def test_get_competition_formats_by_name_individual_sprint(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK, and a body containing one competition_format."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    competition_format_name = competition_format_individual_sprint["name"]
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_individual_sprint
        ],
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats?name={competition_format_name}")
        assert resp.status == HTTPStatus.OK
        assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]
        body = await resp.json()
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
            == competition_format_individual_sprint[
                "max_no_of_contestants_in_raceclass"
            ]
        )
        assert (
            body[0]["max_no_of_contestants_in_race"]
            == competition_format_individual_sprint["max_no_of_contestants_in_race"]
        )


@pytest.mark.integration
async def test_update_competition_format_interval_start(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    new_name = "Oslo Skagen competition-format"
    request_body = deepcopy(competition_format_interval_start)
    request_body["id"] = competition_format_id
    request_body["name"] = new_name

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.NO_CONTENT


@pytest.mark.integration
async def test_update_competition_format_individual_sprint(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id}
        | competition_format_individual_sprint,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value={"id": competition_format_id}
        | competition_format_individual_sprint,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    new_name = "Oslo Skagen competition-format"
    request_body = deepcopy(competition_format_individual_sprint)
    request_body["id"] = competition_format_id
    request_body["name"] = new_name

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.NO_CONTENT


@pytest.mark.integration
async def test_get_all_competition_formats(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return OK and a valid json body."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_all_competition_formats",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start,
            {"id": competition_format_id} | competition_format_individual_sprint,
        ],
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.get("/competition-formats")
        assert resp.status == HTTPStatus.OK
        assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]
        body = await resp.json()
        assert type(body) is list
        assert len(body) > 0
        assert body[0]["id"] == competition_format_id


@pytest.mark.integration
async def test_delete_competition_format_by_id(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=competition_format_id,
    )
    headers = {
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.delete(
            f"/competition-formats/{competition_format_id}", headers=headers
        )
        assert resp.status == HTTPStatus.NO_CONTENT


# Bad cases


@pytest.mark.integration
async def test_create_competition_format_interval_start_unknown_datatype(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return Created, location header."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = deepcopy(competition_format_interval_start)
    request_body["datatype"] = "unknown"

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.BAD_REQUEST


@pytest.mark.integration
async def test_create_competition_format_interval_start_already_exist(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 400 Bad request entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[{id: competition_format_id} | competition_format_interval_start],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = competition_format_interval_start

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.BAD_REQUEST


# Mandatory properties missing at create and update:
@pytest.mark.integration
async def test_create_competition_format_missing_mandatory_property(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = {"optional_property": "Optional_property"}
    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_with_input_id(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = {"id": competition_format_id} | competition_format_interval_start
    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_adapter_fails(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 400 HTTPBadRequest."""
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=None,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=None,
    )
    request_body = competition_format_interval_start
    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.BAD_REQUEST


@pytest.mark.integration
async def test_update_competition_format_unknown_datatype(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return No Content."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    request_body = deepcopy(competition_format_interval_start)
    request_body["datatype"] = "unknown"

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.BAD_REQUEST


@pytest.mark.integration
async def test_update_competition_format_by_id_missing_mandatory_property(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_id,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    request_body = {
        "id": competition_format_id,
        "optional_property": "Optional_property",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_update_competition_format_by_id_different_id_in_body(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 HTTPUnprocessableEntity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_id,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    request_body = {"id": "different_id"} | competition_format_interval_start

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_intervals(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_with_invalid_intervals = deepcopy(
        competition_format_interval_start
    )
    competition_format_with_invalid_intervals["intervals"] = "99:99:99"

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_with_invalid_intervals,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_groups(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_with_invalid_time_between_groups = deepcopy(
        competition_format_interval_start
    )
    competition_format_with_invalid_time_between_groups["time_between_groups"] = (
        "99:99:99"
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_with_invalid_time_between_groups,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_rounds(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_with_invalid_time_between_rounds = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_with_invalid_time_between_rounds["time_between_rounds"] = (
        "99:99:99"
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_with_invalid_time_between_rounds,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_invalid_time_between_heats(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_with_invalid_time_between_heats = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_with_invalid_time_between_heats["time_between_heats"] = (
        "00:00:00"
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_with_invalid_time_between_heats,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_race_config_non_ranked(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["race_config_non_ranked"] = []

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_without_race_config,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_race_config_ranked(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["race_config_ranked"] = []

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_without_race_config,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_rounds_non_ranked_classes(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["rounds_non_ranked_classes"] = []

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_without_race_config,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_competition_format_no_rounds_ranked_classes(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_individual_sprint: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    competition_format_without_race_config = deepcopy(
        competition_format_individual_sprint
    )
    competition_format_without_race_config["rounds_ranked_classes"] = []

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.post(
            "/competition-formats",
            headers=headers,
            json=competition_format_without_race_config,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_update_competition_format_invalid_interval(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 422 Unprocessable Entity."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    updated_competition_format = deepcopy(competition_format_interval_start)
    updated_competition_format["id"] = competition_format_id
    updated_competition_format["intervals"] = "99:99:99"

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=updated_competition_format,
        )
        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY


# Unauthorized cases:


@pytest.mark.integration
async def test_create_competition_format_no_authorization(
    client: _TestClient, mocker: MockFixture, competition_format_interval_start: dict
) -> None:
    """Should return 401 Unauthorized."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )

    request_body = {"name": "Oslo Skagen sprint"}
    headers = MultiDict([(hdrs.CONTENT_TYPE, "application/json")])

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize", status=401)

        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
async def test_update_competition_format_by_id_no_authorization(
    client: _TestClient,
    mocker: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 401 Unauthorized."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value={"id": competition_format_id} | competition_format_interval_start,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=competition_format_id,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
    }

    request_body = {"id": competition_format_id, "name": "Oslo Skagen sprint Oppdatert"}

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize", status=401)

        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
async def test_delete_competition_format_by_id_no_authorization(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 401 Unauthorized."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=competition_format_id,
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize", status=401)

        resp = await client.delete(f"/competition-formats/{competition_format_id}")
        assert resp.status == HTTPStatus.UNAUTHORIZED


# Forbidden:
@pytest.mark.integration
async def test_create_competition_format_insufficient_role(
    client: _TestClient,
    mocker: MockFixture,
    token_unsufficient_role: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 403 Forbidden."""
    competition_format_id = "290e70d5-0933-4af0-bb53-1d705ba7eb95"
    mocker.patch(
        "competition_format_service.services.competition_formats_service.create_id",
        return_value=competition_format_id,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[
            {"id": competition_format_id} | competition_format_interval_start
        ],
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.create_competition_format",
        return_value=competition_format_id,
    )
    request_body = {"name": "Oslo Skagen sprint"}
    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token_unsufficient_role}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize", status=403)
        resp = await client.post(
            "/competition-formats", headers=headers, json=request_body
        )
        assert resp.status == HTTPStatus.FORBIDDEN


# NOT FOUND CASES:


@pytest.mark.integration
async def test_get_competition_format_not_found(
    client: _TestClient,
    mocker: MockFixture,
) -> None:
    """Should return 404 Not found."""
    competition_format_id = "does-not-exist"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats/{competition_format_id}")
        assert resp.status == HTTPStatus.NOT_FOUND


@pytest.mark.integration
async def test_get_competition_formats_by_name_not_found(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 200 OK and empty list."""
    competition_format_name = "does-not-exist"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_formats_by_name",
        return_value=[],
    )

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )

        resp = await client.get(f"/competition-formats?name={competition_format_name}")
        assert resp.status == HTTPStatus.OK
        body = await resp.json()
        assert type(body) is list
        assert len(body) == 0


@pytest.mark.integration
async def test_update_competition_format_not_found(
    client: _TestClient,
    mocker: MockFixture,
    token: MockFixture,
    competition_format_interval_start: dict,
) -> None:
    """Should return 404 Not found."""
    competition_format_id = "does-not-exist"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.update_competition_format",
        return_value=None,
    )

    headers = {
        hdrs.CONTENT_TYPE: "application/json",
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }
    request_body = competition_format_interval_start

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post(
            f"http://{USERS_HOST_SERVER}:{USERS_HOST_PORT}/authorize",
            status=HTTPStatus.NO_CONTENT,
        )
        resp = await client.put(
            f"/competition-formats/{competition_format_id}",
            headers=headers,
            json=request_body,
        )
        assert resp.status == HTTPStatus.NOT_FOUND


@pytest.mark.integration
async def test_delete_competition_format_not_found(
    client: _TestClient, mocker: MockFixture, token: MockFixture
) -> None:
    """Should return 404 Not found."""
    competition_format_id = "does-not-exist"
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.get_competition_format_by_id",
        return_value=None,
    )
    mocker.patch(
        "competition_format_service.adapters.competition_formats_adapter.CompetitionFormatsAdapter.delete_competition_format",
        return_value=None,
    )

    headers = {
        hdrs.AUTHORIZATION: f"Bearer {token}",
    }

    with aioresponses(passthrough=["http://127.0.0.1"]) as m:
        m.post("http://localhost:8081/authorize", status=HTTPStatus.NO_CONTENT)
        resp = await client.delete(
            f"/competition-formats/{competition_format_id}", headers=headers
        )
        assert resp.status == HTTPStatus.NOT_FOUND
