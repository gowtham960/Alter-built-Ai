import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Provider-agnostic connection string. Point this at a local Postgres (default,
# via docker-compose) or at a Supabase connection string with no code changes.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://alterbuilt:alterbuilt@localhost:5432/alterbuilt",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
