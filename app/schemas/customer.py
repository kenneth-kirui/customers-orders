from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field

class Customer(BaseModel):
  name: str
  email: EmailStr
  phone_number: str = Field(default='254718536999')
  password: str
  disable: bool

class CustomerCreate(Customer):
  pass

class CustomerInDb(Customer):
  id: int
  name: str
  email: EmailStr
  password: str
  disable:bool
  created_at:datetime

  class Config:
        orm_mode = True

class UpdateCustomer(Customer):
  created_at:datetime
  


