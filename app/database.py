from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .config import settings


SQLACHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLACHEMY_DATABASE_URL)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)


def get_session():
  with Session(engine) as session:
    yield session