import pytest
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

from app.schemas.tables import InfoTable, CreateTable

T = TypeVar("T", bound=BaseModel)


def validate_response(model: Type[T], data: dict):
    try:
        model.model_validate(data)
        return True
    except ValidationError as e:
        pytest.fail(f"Ошибка валидации: {e}")


@pytest.mark.asyncio
async def test_get_tables(async_client, mock_table_dao_find_all):
    response = await async_client.get("tables/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all([validate_response(InfoTable, item) for item in data])


@pytest.mark.asyncio
async def test_create_table(async_client, mock_table_dao_add):
    data = CreateTable(name="Test table", seats=3, location="test location")
    response = await async_client.post("tables/", content=data.model_dump_json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert validate_response(InfoTable, data)


@pytest.mark.asyncio
async def test_delete_table(async_client, mock_table_dao_delete):
    response = await async_client.delete("tables/", params={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Стол удален"


@pytest.mark.asyncio
async def test_delete_table_not_found(async_client, mock_table_dao_delete_not_found):
    response = await async_client.delete("tables/", params={"id": 2})
    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Стол не найден"
