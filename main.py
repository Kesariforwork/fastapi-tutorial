from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Bookstore with PostgreSQL")


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Bookstore API!"}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books")
def create_book(title: str, author: str, description: str, db: Session = Depends(get_db)):
    book = models.Book(title=title, author=author, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, title: str, author: str, description: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = title
    book.author = author
    book.description = description
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book with id {book_id} deleted successfully"}
