from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import TableDAO
from dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from schemas.tables import IDTable, InfoTable, CreateTable

router = APIRouter()

@router.get('/')
async def get_tables(
        session: AsyncSession = Depends(get_session_without_commit)
) -> list[InfoTable]:
    table_dao = TableDAO(session)
    tables = await table_dao.find_all()
    return [InfoTable.model_validate(table) for table in tables]


@router.post('/')
async def create_table(
        table: CreateTable,
        session: AsyncSession = Depends(get_session_with_commit)
) -> InfoTable:
    table_dao = TableDAO(session)
    new_table = await table_dao.add(table)
    return InfoTable.model_validate(new_table)


@router.delete('/')
async def delete_table(
        table: IDTable,
        session: AsyncSession = Depends(get_session_with_commit)
) -> JSONResponse:
    table_dao = TableDAO(session)
    await table_dao.delete(table)
    return JSONResponse(content={"message": "Стол удален"},
                        status_code=status.HTTP_204_NO_CONTENT)
