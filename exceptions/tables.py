from fastapi import status, HTTPException


class BadRequestCreateTableException(HTTPException):
    def __init__(self,
                 detail = None,
                 status_code = status.HTTP_400_BAD_REQUEST,
                 ):
        msg = f"Переданы не корректные значения стола: {detail}"
        super().__init__(status_code, msg)
