from fastapi import HTTPException, status
from sqlmodel import select

from ..utilities.services import get_password_hash
from ..models.model import Customer

def create_customer(user, session):
    user_in_db = session.exec(select(Customer).where(Customer.email == user.email)).first()
    if user_in_db:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" User with the email {user.email} already exist")
    password = get_password_hash(user.password)
    db_customer = Customer(name=user.name, email=user.email, phone_number = user.phone_number, password=password, disable=user.disable)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

def get_all_Customers(session,offset,limit) :
   customers = session.exec(select(Customer).offset(offset).limit(limit)).all()
   if not customers:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No customers in database")
   return customers

def get_customer(email, session):
   statement = select(Customer).where(Customer.email == email)
   customer = session.exec(statement).first() 
   return customer

def delete_customer(id, session):
   customer = session.get(Customer,id)
   if not customer:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer not found")
   session.delete(customer)
   session.commit()
   return {"ok": True}

def update_customer(id, customer, session):
   customer_in_db = session.get(Customer,id)
   if not customer_in_db:
      raise HTTPException(status_code=404, detail='Customer not found')
   customer_data = customer.dict(exclude_unset=True)
   for field, value in customer_data.items():
      setattr(customer_in_db, field, value)
   session.commit()
   session.refresh(customer_in_db)
   return customer_in_db
  