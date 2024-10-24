import pytest
from .database import client, session
from app.schemas import token
from app.config import settings
import jwt
def test_root(client):
  res = client.get("/")
  assert res.json().get('message')=='Customers orders database'
  assert res.status_code == 200

def test_create_customer(client):
  res = client.post("/customer/",
                     json={"name": "kenneth kirui", 
                                    "email": "kiruikenth@gmail.com",
                                    "phone_number": "254718676999",
                                    "password": "Password123",
                                    "disable":False}) 
  assert res.status_code == 201

def test_login_for_access_token(client,test_customer):
  res  = client.post(
    "/login", data={"username":test_customer['email'], "password":test_customer['password']}
  )
  login_res = token.Token(**res.json())
  payload = jwt.decode(login_res.access_token,settings.secret_key, settings.algorithm)
  id = payload.get("id")
  assert login_res.token_type == "bearer"
  assert res.status_code == 200
