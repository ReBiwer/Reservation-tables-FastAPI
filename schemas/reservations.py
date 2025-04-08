import datetime

from pydantic import BaseModel, Field, ConfigDict
from schemas.tables import InfoTable, IDTable

class BaseReservation(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDReservation(BaseReservation):
    id: int = Field(description="ID брони")


class InfoReservation(IDReservation):
    customer_name: str = Field(description="Имя клиента", examples=["Владимир"])
    reservation_time: datetime.datetime = Field(
        description="Время брони",
        examples=[datetime.datetime.now() + datetime.timedelta(days=1)]
    )
    duration_minutes: int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table: InfoTable = Field(description="Столик брони")

class CreateReservation(BaseReservation):
    customer_name: str = Field(description="Имя клиента", examples=["Владимир"])
    reservation_time: datetime.datetime = Field(
        description="Время брони",
        examples=[datetime.datetime.now() + datetime.timedelta(days=1)]
    )
    duration_minutes: int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table_id: int = Field(description="ID столика брони")
