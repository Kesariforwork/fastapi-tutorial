# models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    author = Column(String(128))
    description = Column(Text)
