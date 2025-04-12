FROM python:3.12

WORKDIR /fastapi_app

COPY .env /fastapi_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/fastapi_app"

COPY /app /fastapi_app/app
COPY alembic.ini /fastapi_app
CMD alembic upgrade head && \
    python app/main.py
