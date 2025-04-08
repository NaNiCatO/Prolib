from fastapi import FastAPI, HTTPException, Body
from typing import List, Optional
from Prolog_Controller import PrologBookManager
from pydantic import BaseModel
import redis
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
manager = PrologBookManager("books.pl")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Allow all origins (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify domains: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class BookUpdate(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    description: Optional[str] = None
    pageCount: Optional[str] = None
    categories: Optional[List[str]] = None
    language: Optional[str] = None
    coverUrl: Optional[str] = None
    isFavorite: Optional[bool] = None  # keep if still needed



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
        data["isCustomBook"] = data["isCustomBook"] == "True"
        data["isFavorite"] = data["isFavorite"] == "True"
        books.append(Book(id=key.split(":")[1], data=data))
    return books

@app.get("/books/{book_id}")
def get_single_book(book_id: str):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    data = r.hgetall(key)

    # Decode fields
    try:
        data["Authors"] = json.loads(data["Authors"])
    except:
        data["Authors"] = []
    try:
        data["Categories"] = json.loads(data["Categories"])
    except:
        data["Categories"] = []
    data["isFavorite"] = data["isFavorite"] == "True"
    data["isCustomBook"] = data["isCustomBook"] == "True"

    return {
        "id": book_id,
        "data": data
    }


@app.patch("/books/{book_id}")
def update_book(book_id: str, update: BookUpdate):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    updates = {}
    for field, value in update.model_dump(exclude_unset=True).items():
        # Convert lists to JSON strings for Redis
        if isinstance(value, list):
            updates[field] = json.dumps(value)
        elif isinstance(value, bool):
            updates[field] = str(value)
        else:
            updates[field] = value

    r.hset(key, mapping=updates)
    return {"message": "Book updated successfully", "updated_fields": list(updates.keys())}

