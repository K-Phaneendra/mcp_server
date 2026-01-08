from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify database connectivity
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    yield

    # Shutdown: clean up engine
    await engine.dispose()