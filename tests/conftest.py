import datetime

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from schemas.tables import InfoTable
from schemas.reservations import InfoReservation
from main import app


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
            base_url="http://test/",
            transport=ASGITransport(app=app)
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def mock_session(mocker):
    session = mocker.MagicMock()
    session.commit = mocker.AsyncMock()
    yield session


@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_add(mocker, mock_session):
    data = InfoTable(id=1, name="Test table", seats=3, location="test location")
    mock_data = data.model_dump()
    mocker.patch(
        "dao.dao.TableDAO.add",
        new_callable=AsyncMock,
        return_value=mock_data
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=mock_session
    )


@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_delete(mocker, mock_session):
        mocker.patch(
            "dao.dao.TableDAO.delete",
        new_callable=AsyncMock,
        return_value=1
        )
        mocker.patch(
            "routers.table_router.get_session_with_commit",
            return_value=mock_session
        )

@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_delete_not_found(mocker, mock_session):
    mocker.patch(
        "dao.dao.TableDAO.delete",
        new_callable=AsyncMock,
        return_value=0
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=mock_session
    )

@pytest_asyncio.fixture(scope="function")
async def mock_reservation_dao_find_all(mocker, mock_session):
    data = [
      {
        "id": 12,
        "customer_name": "Владимир",
        "reservation_time": datetime.datetime(year=2025, month=4, day=20, hour=16, minute=30),
        "duration_minutes": 30,
        "table": {
          "id": 6,
          "name": "Table 3",
          "seats": 2,
          "location": "зал у окна"
        }
      },
      {
        "id": 13,
        "customer_name": "Владимир",
        "reservation_time": datetime.datetime(year=2025, month=4, day=12, hour=16, minute=30),
        "duration_minutes": 30,
        "table": {
          "id": 6,
          "name": "Table 3",
          "seats": 2,
          "location": "зал у окна"
        }
      }
    ]
    mocker.patch(
        "dao.dao.ReservationDAO.find_all",
        new_callable=AsyncMock,
        return_value=data
    )
    mocker.patch(
        "routers.reservation_router.get_session_without_commit",
        return_value=mock_session
    )


@pytest_asyncio.fixture(scope="function")
async def mock_reservation_dao_add(mocker, mock_session):
    data = (
        InfoReservation(
            id=1,
            customer_name="Владимир",
            reservation_time=datetime.datetime(year=2025, month=4, day=12, hour=16, minute=30),
            duration_minutes=30,
            table=InfoTable(
                id=1,
                name="Test table",
                seats=3,
                location="test location"
            )
        )
    )
    mock_data = data.model_dump()
    mocker.patch(
        "dao.dao.ReservationDAO.add",
        new_callable=AsyncMock,
        return_value=mock_data
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=mock_session
    )

@pytest_asyncio.fixture(scope="function")
async def mock_reservation_dao_delete(mocker, mock_session):
        mocker.patch(
            "dao.dao.ReservationDAO.delete",
        new_callable=AsyncMock,
        return_value=1
        )
        mocker.patch(
            "routers.table_router.get_session_with_commit",
            return_value=mock_session
        )

@pytest_asyncio.fixture(scope="function")
async def mock_reservation_dao_delete_not_found(mocker, mock_session):
    mocker.patch(
        "dao.dao.ReservationDAO.delete",
        new_callable=AsyncMock,
        return_value=0
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=mock_session
    )


