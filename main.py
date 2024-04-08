from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from pymongo import MongoClient

books = [
    {"id": 1, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "quantity": 5},
    {"id": 2, "title": "Pride and Prejudice", "author": "Jane Austen", "quantity": 3},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 2},
    {"id": 4, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "quantity": 1},
    {"id": 5, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "quantity": 4},
]

def get_book_details(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    return None

client = MongoClient("mongodb://localhost:27017") 
db = client["Library"]  
borrowings_collection = db["borrowings"]

app = FastAPI()

# Data models for books and borrowing records

class Book(BaseModel):
    id: int
    title: str
    author: str
    quantity: int

class BorrowedBook(BaseModel):
    book_id: int
    borrowed_date: datetime = datetime.now()
    returned_date: datetime = None  

class Borrowing(BaseModel):
    member_id: int  
    borrowed_books: List[BorrowedBook]

class BorrowingConfirmation(BaseModel):
    id: int
    timestamp: str
    borrowed_books: List[BorrowedBook]


# API Endpoints

@app.get("/")
async def base():
    return "Library Management System API is running"

@app.get("/books", response_model=List[Book])
async def get_books():
    return books

@app.post("/borrowings", response_model=BorrowingConfirmation)
async def create_borrowing(borrowing: Borrowing):
    confirmation = BorrowingConfirmation()
    confirmation.timestamp = str(datetime.now())
    confirmation.borrowed_books = []

    for borrowed_book in borrowing.borrowed_books:
        book_details = get_book_details(borrowed_book.book_id)
        if book_details is None:
            raise HTTPException(status_code=404, detail=f"Book with ID {borrowed_book.book_id} not found")

        if book_details["quantity"] <= 0:
            raise HTTPException(status_code=400, detail=f"Book with ID {borrowed_book.book_id} is not available for borrowing")

        book_details["quantity"] -= 1
        confirmation.borrowed_books.append(borrowed_book)

    borrowing_data = borrowing.dict()
    borrowings_collection.insert_one(borrowing_data)
    confirmation.id = borrowings_collection.count_documents({}) + 1

    return confirmation

@app.get("/borrowings", response_model=List[BorrowingConfirmation])
async def get_borrowings(skip: int = 0, limit: int = 10):
    cursor = borrowings_collection.find().skip(skip).limit(limit)
    borrowings_list = [BorrowingConfirmation(**borrowing) for borrowing in cursor]
    return borrowings_list

@app.get("/borrowings/{borrowing_id}", response_model=BorrowingConfirmation)
async def get_borrowing(borrowing_id: int):
    borrowing_data = borrowings_collection.find_one({"id": borrowing_id})
    if borrowing_data:
        return BorrowingConfirmation(**borrowing_data)
    return None

@app.put("/borrowings/{borrowing_id}/return")
async def return_book(borrowing_id: int):
    borrowing_data = borrowings_collection.find_one({"id": borrowing_id})
    if borrowing_data is None:
        raise HTTPException(status_code=404, detail=f"Borrowing with ID {borrowing_id} not found")
    
    borrowings_collection.update_one({"id": borrowing_id}, {"$set": {"returned_date": datetime.now()}})
