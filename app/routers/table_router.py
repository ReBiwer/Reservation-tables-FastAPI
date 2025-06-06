from fastapi import APIRouter, Depends
from fastapi import status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.tables import BadRequestCreateTableException
from app.dao.dao import TableDAO
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.schemas.tables import IDTable, InfoTable, CreateTable

router = APIRouter()

@router.get('/', summary="Получить список столов")
async def get_tables(
        session: AsyncSession = Depends(get_session_without_commit)
) -> list[InfoTable]:
    table_dao = TableDAO(session)
    try:
        tables = await table_dao.find_all()
        return [InfoTable.model_validate(table) for table in tables]
    except SQLAlchemyError as e:
        raise BadRequestCreateTableException(e)


@router.post('/', summary="Добавить стол")
async def create_table(
        table: CreateTable,
        session: AsyncSession = Depends(get_session_with_commit)
) -> InfoTable:
    table_dao = TableDAO(session)
    try:
        new_table = await table_dao.add(table)
        return InfoTable.model_validate(new_table)
    except SQLAlchemyError as e:
        raise BadRequestCreateTableException(e)


@router.delete('/', summary="Удалить стол")
async def delete_table(
        table: IDTable = Query(title="ID стола", description="Идентификатор стола для удаления"),
        session: AsyncSession = Depends(get_session_with_commit)
) -> JSONResponse:
    table_dao = TableDAO(session)
    try:
        count_del = await table_dao.delete(table)
        if count_del == 0:
            return JSONResponse(content={"message": "Стол не найден"}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content={"message": "Стол удален"}, status_code=status.HTTP_200_OK)
    except SQLAlchemyError as e:
        raise BadRequestCreateTableException(e)