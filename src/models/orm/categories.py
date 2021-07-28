from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    name = Column(String(length=255))

    subcategories = relationship("SubCategory", back_populates="category")


class SubCategory(BaseModel):
    category_id = Column(Integer, ForeignKey(Category.get_foreign_attr("id")))
    name = Column(String(length=255))

    category = relationship(Category.referent(), back_populates="subcategories")
