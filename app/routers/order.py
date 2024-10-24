from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, Query,BackgroundTasks, HTTPException, status
from sqlmodel import Session
from app.routers.auth import get_current_active_user
from ..schemas.order import CreateOrder, OrdersInDb, UpdateOrder
from ..models import model
from ..crud import ordercrud
from ..database import get_session
from backgroundtasks.sendsms import sendmessage

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
  prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_router(order:CreateOrder, session:SessionDep,background_tasks: BackgroundTasks, current_user: Annotated[model.Customer, Depends(get_current_active_user)]):
  phone_number = '+'+current_user.phone_number
  message = f"Your order, {order.item}, was placed successfully."
  background_tasks.add_task(sendmessage, phone_number, message)
  return ordercrud.create_order(order=order, session=session)

@router.get("/")
def get_orders(session:SessionDep, 
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 100,) -> list[OrdersInDb]:
  return ordercrud.get_all_orders(session=session, offset=offset, limit=limit)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id, session:SessionDep):
  return ordercrud.delete_order(id=id, session=session)

@router.put("/{id}")
def update_customer(id, order_data:UpdateOrder, session:SessionDep):
  return ordercrud.update_order(id=id, order_data=order_data, session=session)

@router.post("/search/")
def search_order(session:SessionDep,
                 start_date: datetime = Form(...), 
                 end_date: datetime = Form(...),
                ) -> list[OrdersInDb]:
  return ordercrud.search_order(start_date=start_date, end_date=end_date, session=session)


