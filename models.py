import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_uniq


class Table(Base):
    name: Mapped[str_uniq]
    seats: Mapped[int]
    location: Mapped[str]

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="table")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class Reservation(Base):
    customer_name: Mapped[str]
    reservation_time: Mapped[datetime.datetime]
    duration_minutes: Mapped[int]

    table_id: Mapped[int] = mapped_column(ForeignKey('tables.id'))
    table: Mapped["Table"] = relationship("Table", back_populates="reservations", lazy="joined")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, customer_name={self.customer_name})"
