from fastapi import FastAPI, HTTPException, Body
from typing import List, Optional
from Prolog_Controller import PrologBookManager
from pydantic import BaseModel
import redis
import json
from fastapi.middleware.cors import CORSMiddleware
import uuid
from NLPPipeline import NLPPipeline

app = FastAPI()
manager = PrologBookManager("books.pl")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
chatbot = NLPPipeline()

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
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    description: Optional[str] = None
    isbn10: Optional[str] = None
    isbn13: Optional[str] = None
    pageCount: Optional[str] = None
    categories: Optional[List[str]] = None
    language: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    averageRating: Optional[float] = None
    ratingsCount: Optional[int] = None
    previewLink: Optional[str] = None
    infoLink: Optional[str] = None
    


# 1. Get by ISBN
@app.get("/book/{isbn13}")
def get_by_id(isbn13: str):
    book = manager.get_by_isbn(isbn13)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 2. Remove by ISBN
@app.delete("/book/{isbn13}")
def remove_by_id(isbn13: str):
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
def edit_by_id(isbn13: str, book: dict = Body(...)):
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

# 9. Query all books from Redis
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

# 10. Get a single book by ID from Redis
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

# 11. Add a book to Redis
@app.post("/books")
def add_book(book: Book):
    book_id = str(uuid.uuid4())
    key = f"book:{book_id}"

    # Convert lists to JSON strings for Redis
    book_data = {
        "Title": book.title,
        "Authors": json.dumps(book.authors) if book.authors else None,
        "Publisher": book.publisher,
        "Published Date": book.publishedDate,
        "Description": book.description,
        "ISBN 10": book.isbn10,
        "ISBN 13": book.isbn13,
        "Page Count": book.pageCount,
        "Categories": json.dumps(book.categories) if book.categories else None,
        "Language": book.language,
        "Thumbnail URL": book.thumbnailUrl,
        "Average Rating": str(book.averageRating) if book.averageRating else None,
        "People Rated": str(book.ratingsCount) if book.ratingsCount else None,
        "Preview Link": book.previewLink,
        "Info Link": book.infoLink
    }
    # Add to Prolog database
    book_data["Id"] = book_id
    manager.create(book_data)

    # remove 'Id' from book_data for Redis
    book_data.pop("Id", None)
    # Add isFavorite and isCustomBook fields
    book_data["isFavorite"] = False
    book_data["isCustomBook"] = True

    r.hset(key, mapping=book_data)


    
    return {"id": book_id, **book_data}

# 12. Update a book in Redis
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

    # Update Prolog database
    book = manager.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in Prolog database")
    
    # Update the Prolog database with the new values
    for field, value in updates.items():
        if field == "Title":
            book["Title"] = value
        elif field == "Authors":
            book["Authors"] = value
        elif field == "Publisher":
            book["Publisher"] = value
        elif field == "Published Date":
            book["Published Date"] = value
        elif field == "Description":
            book["Description"] = value
        elif field == "Page Count":
            book["Page Count"] = value
        elif field == "Categories":
            book["Categories"] = value
        elif field == "Language":
            book["Language"] = value
        else:
            continue
    manager.edit_by_id(book_id, book)

    return {"message": "Book updated successfully", "updated_fields": list(updates.keys())}

# 13. Delete a book from Redis
@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    # Remove from Prolog database
    manager.remove_by_id(book_id)

    # Remove from Redis
    r.delete(key)
    return {"detail": "Book deleted successfully"}

# 14. Toggle favorite status
@app.patch("/books/{book_id}/favorite")
def toggle_favorite(book_id: str):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    current_status = r.hget(key, "isFavorite")
    new_status = not (current_status == "True")
    r.hset(key, "isFavorite", str(new_status))

    return {"detail": "Favorite status updated", "isFavorite": new_status}

# 15. NLP Query
@app.post("/nlp_query")
def nlp_query(query: str):
    result, book_ID = chatbot.run(query)
    return {"result": result, "book_ID": book_ID}