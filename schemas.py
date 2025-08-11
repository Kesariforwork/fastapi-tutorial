# schemas.py
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str | None = None
    description: str | None = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True
