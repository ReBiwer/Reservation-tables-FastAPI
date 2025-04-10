from fastapi import status, HTTPException


class CreateReservationException(HTTPException):
    def __init__(self,
                 status_code = status.HTTP_409_CONFLICT,
                 detail = "Нельзя создать бронь на этот временной слот и на этот столик"
                 ):
        super().__init__(status_code, detail)


class BadRequestCreateReservationException(HTTPException):
    def __init__(self,
                 detail = None,
                 status_code = status.HTTP_400_BAD_REQUEST,
                 ):
        msg = f"Переданы не корректные значения брони: {detail}"
        super().__init__(status_code, msg)
