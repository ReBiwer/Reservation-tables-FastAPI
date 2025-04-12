from loguru import logger
from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.reservations import CreateReservationException
from app.schemas.reservations import CreateReservation
from app.dao.base import BaseDAO
from app.models import Table, Reservation


class TableDAO(BaseDAO):
    model = Table

class ReservationDAO(BaseDAO):
    model = Reservation

    async def check_instance(self, values: CreateReservation):
        values_dict = values.model_dump()
        result = await self._session.execute(
            select(
                exists().where(
                    (
                        ((self.model.reservation_time >= values_dict.get("reservation_time")) &
                         (self.model.reservation_time <= values_dict.get("duration_minutes"))) |
                        ((self.model.duration_minutes >= values_dict.get("reservation_time")) &
                         (self.model.duration_minutes <= values_dict.get("duration_minutes"))) |
                        ((values_dict.get("reservation_time") >= self.model.reservation_time) &
                         (values_dict.get("reservation_time") <= self.model.duration_minutes))
                    ) &
                    (self.model.table_id == values.table_id)
                )
            )
        )
        return result.scalar()

    async def add(self, values: CreateReservation):
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values_dict}")
        try:
            new_instance = self.model(**values_dict)
            if await self.check_instance(values):
                logger.info(f"Запись {self.model.__name__} с параметрами: {values_dict} уже существует")
                raise CreateReservationException()
            self._session.add(new_instance)
            logger.info(f"Запись {self.model.__name__} успешно добавлена.")
            await self._session.commit()
            await self._session.refresh(new_instance)
            return new_instance
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise
