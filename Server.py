from fastapi import FastAPI, HTTPException, Body
from typing import List, Optional
from Prolog_Controller import PrologBookManager
from pydantic import BaseModel
import redis
import json

app = FastAPI()
manager = PrologBookManager("books.pl")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# --- Data Models ---
class BookUpdate(BaseModel):
    Fav: Optional[bool] = None

class Book(BaseModel):
    id: str
    data: dict


# 1. Get by ISBN
@app.get("/book/{isbn13}")
def get_by_isbn(isbn13: str):
    book = manager.get_by_isbn(isbn13)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 2. Remove by ISBN
@app.delete("/book/{isbn13}")
def remove_by_isbn(isbn13: str):
    success = manager.remove_by_isbn(isbn13)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found or could not be deleted")
    return {"detail": "Book removed successfully"}

# 3. Create a book
@app.post("/book")
def create(book: dict = Body(...)):
    manager.create(book)
    return {"detail": "Book added successfully"}

# 4. Edit a book
@app.put("/book/{isbn13}")
def edit_by_isbn(isbn13: str, book: dict = Body(...)):
    success = manager.edit_by_isbn(isbn13, book)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found or update failed")
    return {"detail": "Book updated successfully"}

# 5. Query by exact title
@app.get("/query/exact_title")
def query_by_exact_title(title: str):
    return manager.query_by_exact_title(title)

# 6. Query by title keyword
@app.get("/query/title")
def query_by_title(title: str):
    return manager.query_by_title(title)

# 7. Query by author keyword
@app.get("/query/author")
def query_by_author(author: str):
    return manager.query_by_author(author)

# 8. Custom query with multiple fields
@app.post("/query/custom")
def query_custom(filters: dict = Body(...)):
    return manager.query_custom(filters)

@app.get("/books", response_model=List[Book])
def get_all_books():
    keys = r.keys("book:*")
    books = []
    for key in keys:
        data = r.hgetall(key)
        data["Authors"] = json.loads(data["Authors"])
        data["Categories"] = json.loads(data["Categories"])
        data["Fav"] = data["Fav"] == "True"
        books.append(Book(id=key.split(":")[1], data=data))
    return books

@app.patch("/books/{book_id}")
def update_book(book_id: str, update: BookUpdate):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only fields that are set
    if update.Fav is not None:
        r.hset(key, "Fav", str(update.Fav))

    return {"message": "Book updated successfully"}