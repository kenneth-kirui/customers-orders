from fastapi import FastAPI
from app.routers import auth
from .routers import customer, order
from .database import create_db_and_tables
app = FastAPI()

@app.on_event("startup")
def on_startup():
  create_db_and_tables()

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(order.router)
@app.get("/")
def root():
  return {"message":"Customers orders database"}
