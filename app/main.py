from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.routers.table_router import router as table_router
from app.routers.reservation_router import router as reservation_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    try:
        yield
    finally:
        logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    app.include_router(table_router, prefix='/tables', tags=['Tables'])
    app.include_router(reservation_router, prefix='/reservations', tags=['Reservations'])


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
