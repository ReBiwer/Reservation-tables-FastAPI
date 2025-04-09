from fastapi import APIRouter, Depends
from fastapi import status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import ReservationDAO
from dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from schemas.reservations import IDReservation, InfoReservation, CreateReservation

router = APIRouter()

@router.get('/', summary="Получить список броней")
async def get_reservations(
        session: AsyncSession = Depends(get_session_without_commit)
) -> list[InfoReservation]:
    reservation_dao = ReservationDAO(session)
    reservations = await reservation_dao.find_all()
    return [InfoReservation.model_validate(res) for res in reservations]


@router.post('/', summary="Создать бронь")
async def create_reservation(
        reservation: CreateReservation,
        session: AsyncSession = Depends(get_session_with_commit)
) -> InfoReservation:
    reservation_dao = ReservationDAO(session)
    new_reservation = await reservation_dao.add(reservation)
    return InfoReservation.model_validate(new_reservation)


@router.delete('/', summary="Удалить бронь")
async def delete_reservation(
        reservation: IDReservation = Query(title="ID стола", description="Идентификатор стола для удаления"),
        session: AsyncSession = Depends(get_session_with_commit)
) -> JSONResponse:
    reservation_dao = ReservationDAO(session)
    count_del = await reservation_dao.delete(reservation)
    if count_del == 0:
        return JSONResponse(content={"message": "Бронь не найдена"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"message": "Бронь удалена"}, status_code=status.HTTP_200_OK)
