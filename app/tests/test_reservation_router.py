import datetime
import json

import pytest
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

from app.schemas.reservations import InfoReservation, CreateReservation

T = TypeVar("T", bound=BaseModel)


def validate_response(model: Type[T], data: dict):
    try:
        model.model_validate(data)
        return True
    except ValidationError as e:
        pytest.fail(f"Ошибка валидации: {e}")


@pytest.mark.asyncio
async def test_get_reservations(async_client, mock_reservation_dao_find_all):
    response = await async_client.get("reservations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all([validate_response(InfoReservation, item) for item in data])


@pytest.mark.asyncio
async def test_create_reservation(async_client, mock_reservation_dao_add):
    data = {
        "customer_name": "Владимир",
        "reservation_time": "12.04.2025 16:30",
        "duration_minutes": 30,
        "table_id": 1
    }
    response = await async_client.post("reservations/", content=json.dumps(data))
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert validate_response(InfoReservation, data)


@pytest.mark.asyncio
async def test_delete_reservation(async_client, mock_reservation_dao_delete):
    response = await async_client.delete("reservations/", params={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Бронь удалена"


@pytest.mark.asyncio
async def test_delete_table_not_found(async_client, mock_reservation_dao_delete_not_found):
    response = await async_client.delete("reservations/", params={"id": 2})
    print(response.text)
    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Бронь не найдена"
