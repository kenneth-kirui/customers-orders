from datetime import datetime
from pydantic import BaseModel

class Orders(BaseModel):
  item: str
  amount: float
  customer_id: int
  

class CreateOrder(Orders):
  pass

class OrdersInDb(Orders):
  id: int
  created_at: datetime
  
  class Config:
        orm_mode = True

class UpdateOrder(Orders):
   created_at: datetime