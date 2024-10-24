
import datetime
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session

class Customer(SQLModel, table=True):
  id: int |None = Field(default=None, primary_key=True)
  name:str = Field(index=True)
  email: str = Field(index=True)
  password:str=Field()
  phone_number: str=Field(default=None, nullable=False)
  disable:bool = Field(default=False)
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

  orders: list["Order"] = Relationship(back_populates="customer")

class Order(SQLModel, table=True):
  id: int | None  = Field(default=None, primary_key=True)
  item: str = Field(index=True)
  amount: float = Field(index=True)
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

  customer_id:int | None = Field(default=None, foreign_key="customer.id")
  customer: Customer | None = Relationship(back_populates="orders")
  

