from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.products import router
from app.core.database import Base, engine
from app.models import product  # noqa: F401  (registra la tabla)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Product API", version="1.0.0", lifespan=lifespan)
app.include_router(router)
