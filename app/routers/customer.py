from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.routers.auth import get_current_active_user
from ..schemas.customer import CustomerCreate, CustomerInDb, UpdateCustomer
from ..crud import customercrud

from ..database import get_session
from ..models import model

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
  prefix="/customer",
    tags=["customer"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CustomerInDb, status_code=status.HTTP_201_CREATED)
def create_customer(customer:CustomerCreate, session:SessionDep):
  return customercrud.create_customer(user=customer, session=session)

@router.get("/")
def read_all_users(session:SessionDep, offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,) -> list[CustomerInDb]:
  return customercrud.get_all_Customers(session=session, offset=offset, limit=limit)

@router.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id, session:SessionDep, current_user: Annotated[model.Customer, Depends(get_current_active_user)]):
  return customercrud.delete_customer(id=id, session=session)

@router.put("/{id}")
def update_customer(id, customer:UpdateCustomer, session:SessionDep, current_user: Annotated[model.Customer, Depends(get_current_active_user)]):
  return customercrud.update_customer(id=id, customer=customer, session=session)
  
