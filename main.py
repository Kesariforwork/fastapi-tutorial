from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from pydantic import BaseModel
from typing import Optional, List

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Bookstore with PostgreSQL")

# Pydantic model for request body validation
class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None

# Pydantic model for response serialization
class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Bookstore API!"}

@app.get("/books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        description=book.description
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
