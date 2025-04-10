import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer
from schemas.tables import InfoTable, IDTable

class BaseReservation(BaseModel):
    model_config = ConfigDict(
        from_attributes = True,
    )


class IDReservation(BaseReservation):
    id: int = Field(description="ID брони")

example_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
formated_example_datetime = example_datetime.strftime("%d.%m.%Y %H:%M")

class InfoReservation(IDReservation):
    customer_name: str = Field(description="Имя клиента", examples=["Владимир"])
    reservation_time: datetime.datetime = Field(
        description="Время брони",
        examples=[formated_example_datetime],
    )
    duration_minutes: int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table: InfoTable = Field(description="Столик брони")

    @field_serializer("reservation_time", when_used="json")
    def serializer_reservation_time(self, value: datetime.datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M")


class CreateReservation(BaseReservation):
    customer_name: str = Field(description="Имя клиента", examples=["Владимир"])
    reservation_time: datetime.datetime = Field(
        description="Время брони",
        examples=[formated_example_datetime]
    )
    duration_minutes: int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table_id: int = Field(description="ID столика брони")

    @field_validator("reservation_time", mode="before")
    def validate_before__reservation_time(cls, value: str) -> datetime.datetime:
        return datetime.datetime.strptime(value, "%d.%m.%Y %H:%M")
