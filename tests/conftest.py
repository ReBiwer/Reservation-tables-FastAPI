import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from schemas.tables import InfoTable
from main import app


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
            base_url="http://test/",
            transport=ASGITransport(app=app)
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_add(mocker):
    session = mocker.MagicMock()
    session.commit = mocker.AsyncMock()
    data = InfoTable(id=1, name="Test table", seats=3, location="test location")
    mock_data = data.model_dump()
    mocker.patch(
        "dao.dao.TableDAO.add",
        new_callable=AsyncMock,
        return_value=mock_data
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=session
    )

@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_delete(mocker):
    session = mocker.MagicMock()
    session.commit = mocker.AsyncMock()
    mocker.patch(
        "dao.dao.TableDAO.delete",
        new_callable=AsyncMock,
        return_value=1
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=session
    )

@pytest_asyncio.fixture(scope="function")
async def mock_table_dao_delete_not_found(mocker):
    session = mocker.MagicMock()
    session.commit = mocker.AsyncMock()
    mocker.patch(
        "dao.dao.TableDAO.delete",
        new_callable=AsyncMock,
        return_value=0
    )
    mocker.patch(
        "routers.table_router.get_session_with_commit",
        return_value=session
    )
