import contextlib
from typing import AsyncIterator, TypedDict
from fastapi import FastAPI
from animit.health.endpoints import router as health_router
from animit.api import router
from animit.kit.db.postgres import (
    create_async_sessionmaker,
    create_sync_sessionmaker,
    AsyncEngine,
    AsyncSessionMaker,
    Engine,
    SyncSessionMaker,
)
from animit.postgres import (
    AsyncSessionMiddleware,
    create_async_engine,
    create_sync_engine,
)


class State(TypedDict):
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMaker
    async_read_engine: AsyncEngine
    async_read_sessionmaker: AsyncSessionMaker
    sync_engine: Engine
    sync_sessionmaker: SyncSessionMaker


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async_engine = async_read_engine = create_async_engine("app")
    async_sessionmaker = async_read_sessionmaker = create_async_sessionmaker(
        async_engine
    )
    instrument_engines = [async_engine.sync_engine]

    sync_engine = create_sync_engine("app")
    sync_sessionmaker = create_sync_sessionmaker(sync_engine)
    instrument_engines.append(sync_engine)

    yield {
        "async_engine": async_engine,
        "async_sessionmaker": async_sessionmaker,
        "async_read_engine": async_read_engine,
        "async_read_sessionmaker": async_read_sessionmaker,
        "sync_engine": sync_engine,
        "sync_sessionmaker": sync_sessionmaker,
    }

    await async_engine.dispose()
    if async_read_engine is not async_engine:
        await async_read_engine.dispose()
    sync_engine.dispose()


def create_app():
    app = FastAPI(
        lifespan=lifespan,
    )

    app.add_middleware(AsyncSessionMiddleware)

    app.include_router(health_router)

    app.include_router(router)

    return app


app = create_app()
