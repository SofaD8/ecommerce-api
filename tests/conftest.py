import os
from typing import AsyncGenerator
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.session import get_db


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://sofa:postgres@localhost:5432/ecommerce")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
test_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def _override_get_db():
        yield db

    app.dependency_overrides[get_db] = _override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
