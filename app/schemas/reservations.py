import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer

from app.schemas.tables import InfoTable


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
    duration_minutes: datetime.datetime | int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table: InfoTable = Field(description="Столик брони")

    @field_serializer("duration_minutes")
    def serializer_duration_minute(self, value: datetime.datetime) -> int:
        minute = value - self.reservation_time
        return int(minute.seconds / 60)

    @field_serializer("reservation_time")
    def serializer_reservation_time(self, value: datetime.datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M")


    @field_validator("reservation_time", mode="before")
    def validate_reservation_time(cls, value: str | datetime.datetime) -> datetime.datetime:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%d.%m.%Y %H:%M")
        return value


class CreateReservation(BaseReservation):
    customer_name: str = Field(description="Имя клиента", examples=["Владимир"])
    reservation_time: datetime.datetime = Field(
        description="Время брони",
        examples=[formated_example_datetime]
    )
    duration_minutes: int = Field(description="Продолжительность брони в минутах", examples=[30, 60])
    table_id: int = Field(description="ID столика брони")


    @field_serializer("duration_minutes")
    def minutes_to_end_time(self, value: int) -> datetime.datetime:
        return self.reservation_time + datetime.timedelta(minutes=value)


    @field_validator("reservation_time", mode="before")
    def validate_reservation_time(cls, value: str | datetime.datetime) -> datetime.datetime:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, "%d.%m.%Y %H:%M")
        return value
