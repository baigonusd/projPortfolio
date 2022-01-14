from sqlalchemy import Boolean, Column, Text, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel


class Order(BaseModel):
    customer_name: str
    order_quantity: int


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return f"<Item_name={self.name} price={self.price}"
