from dao.base import BaseDAO
from models import Table, Reservation


class TableDAO(BaseDAO):
    model = Table

class ReservationDAO(BaseDAO):
    model = Reservation
