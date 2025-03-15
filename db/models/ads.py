from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Ads(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    product_id: Optional[int] = Field(foreign_key="product.id")
    user: Optional["User"] = Relationship(back_populates="ads")
    product: Optional["Product"] = Relationship(back_populates="ads")
