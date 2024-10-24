
from fastapi import HTTPException, status
from sqlalchemy import select
from app.models.model import Order


def create_order(order, session):
  db_order = Order(item=order.item , amount=order.amount,customer_id=order.customer_id)
  session.add(db_order)
  session.commit()
  session.refresh(db_order)
  return db_order

def get_all_orders(session, offset, limit):
  query = select(Order).offset(offset).limit(limit)
  orders = session.execute(query).scalars().all()
  if not orders:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No customers in database")
  return orders

def delete_order(session, id):
  order = session.get(Order,id)
  if not order:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
  session.delete(order)
  session.commit()
  return {"ok": True}

def update_order(id, order_data, session):
   order = session.get(Order,id)
   if not order:
      raise HTTPException(status_code=404, detail='order not found')
   order_data = order_data.dict(exclude_unset=True)
   for field, value in order_data.items():
      setattr(order, field, value)

   session.commit()
   session.refresh(order)
   return order

def search_order(start_date, end_date, session):
  orders = session.query(Order).filter(Order.created_at >= start_date, Order.created_at <= end_date).all()
  return orders