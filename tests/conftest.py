import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.config import settings
from app.database import get_session
from app.main import app

SQLACHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLACHEMY_DATABASE_URL)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
  SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def session():
  drop_db_and_tables()
  create_db_and_tables()
  with Session(engine) as session:
     yield session

@pytest.fixture(scope="module")
def client(session):
  def overide_get_session():
    yield session
  app.dependency_overrides[get_session] = overide_get_session
  yield TestClient(app)

@pytest.fixture
def test_customer(client):
  customer_data = {
    "name": "kenneth kirui",
    "email": "aron@gmail.com",
    "phone_number": "254718536999",
    "password": "Password123",
    "disable":False
    }
  res = client.post("/customer/", json=customer_data)
  new_customer = res.json()
  new_customer['password']=customer_data['password']
  assert res.status_code == 201
  return  new_customer
  