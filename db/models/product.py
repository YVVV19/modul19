from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator



class Product(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(..., gt=20, lt=100)
    price: float
    status: bool
    ads: List["Ads"] = Relationship(back_populates="product")

    @field_validator('price')
    @classmethod
    def price(cls, v):
        if v <= 0:
            raise ValueError('Price must be over zero!!!')
        return v