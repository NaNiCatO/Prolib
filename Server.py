from fastapi import FastAPI, HTTPException, Body
from typing import List, Optional
from Prolog_Controller import PrologBookManager
from pydantic import BaseModel, Field
import redis
import json
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pprint import pprint
#from NLPPipeline import NLPPipeline

app = FastAPI()
manager = PrologBookManager("books.pl")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# chatbot = NLPPipeline()

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
    title: Optional[str] = Field(default=None, alias="Title")
    authors: Optional[List[str]] = Field(default=None, alias="Authors")
    publisher: Optional[str] = Field(default=None, alias="Publisher")
    publishedDate: Optional[str] = Field(default=None, alias="Published_Date")
    description: Optional[str] = Field(default=None, alias="Description")
    pageCount: Optional[str] = Field(default=None, alias="Page_Count")
    categories: Optional[List[str]] = Field(default=None, alias="Categories")
    language: Optional[str] = Field(default=None, alias="Language")
    coverUrl: Optional[str] = Field(default=None, alias="Thumbnail_URL")

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
    

class BookData(BaseModel):
    Title: str = Field(..., alias="Title")
    Authors: List[str] = Field(..., alias="Authors")
    Publisher: str = Field(..., alias="Publisher")
    Published_Date: str = Field(..., alias="Published Date")
    Description: str = Field(..., alias="Description")
    ISBN_10: str = Field(..., alias="ISBN 10")
    ISBN_13: str = Field(..., alias="ISBN 13")
    Page_Count: str = Field(..., alias="Page Count")
    Categories: List[str] = Field(..., alias="Categories")
    Language: str = Field(..., alias="Language")
    Thumbnail_URL: str = Field(..., alias="Thumbnail URL")
    Average_Rating: Optional[str] = Field(default=None, alias="Average Rating")
    Ratings_Count: Optional[str] = Field(default=None, alias="Ratings Count")
    Preview_Link: Optional[str] = Field(default=None, alias="Preview Link")
    Info_Link: Optional[str] = Field(default=None, alias="Info Link")
    isFavorite: bool = Field(..., alias="isFavorite")
    isCustomBook: bool = Field(..., alias="isCustomBook")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class Books(BaseModel):
    id: str
    data: BookData





def safe_json_list(value, fallback=[]):
    try:
        return json.loads(value) if isinstance(value, str) else value
    except Exception as e:
        print(f"[ERROR] Failed to decode JSON list: {value} -> {e}")
        return fallback
    



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
@app.get("/books", response_model=List[Books])
def get_all_books():
    keys = r.keys("book:*")
    results = []

    for key in keys:
        raw = r.hgetall(key)
        try:
            # Safely decode Authors and Categories (stored as JSON strings)
            raw["Authors"] = safe_json_list(raw.get("Authors", "[]"))
            raw["Categories"] = safe_json_list(raw.get("Categories", "[]"))

            # Booleans come in as strings from Redis
            raw["isFavorite"] = raw.get("isFavorite", "False") == "True"
            raw["isCustomBook"] = raw.get("isCustomBook", "False") == "True"

            ## Handle missing fields gracefully
            raw["Average Rating"] = None if raw.get("Average Rating") == "None" else raw.get("Average Rating")
            raw["Ratings Count"] = None if raw.get("Ratings Count") == "None" else raw.get("Ratings Count")

            raw["Preview Link"] = "" if raw.get("Preview Link") == "None" else raw.get("Preview Link")
            raw["Info Link"] = "" if raw.get("Info Link") == "None" else raw.get("Info Link")

            # Parse into BookData and Books model
            book_data = BookData(**raw)
            book = Books(id=key.split(":")[1], data=book_data)
            results.append(book)

        except Exception as e:
            print(f"[ERROR] Skipping book in key {key}: {e}")
            print("Raw Redis data:", raw)

    return results


# 10. Get a single book by ID from Redis
@app.get("/books/{book_id}", response_model=Books)
def get_single_book(book_id: str):
    key = f"book:{book_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Book not found")

    raw = r.hgetall(key)

    try:
        raw["Authors"] = safe_json_list(raw.get("Authors", "[]"))
        raw["Categories"] = safe_json_list(raw.get("Categories", "[]"))
        raw["isFavorite"] = raw.get("isFavorite", "False") == "True"
        raw["isCustomBook"] = raw.get("isCustomBook", "False") == "True"

        ## Handle missing fields gracefully
        raw["Average Rating"] = None if raw.get("Average Rating") == "None" else raw.get("Average Rating")
        raw["Ratings Count"] = None if raw.get("Ratings Count") == "None" else raw.get("Ratings Count")

        raw["Preview Link"] = "" if raw.get("Preview Link") == "None" else raw.get("Preview Link")
        raw["Info Link"] = "" if raw.get("Info Link") == "None" else raw.get("Info Link")

        book_data = BookData(**raw)
        return Books(id=book_id, data=book_data)

    except Exception as e:
        print(f"[ERROR] Failed to parse book with ID {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Error parsing book")



# 11. Add a book to Redis
@app.post("/books", response_model=Books)
def add_book(book: Books):
    book_id = str(uuid.uuid4())
    key = f"book:{book_id}"

    data = book.data
    print(data)

    # Prepare Redis-friendly format
    redis_data = {
        "Title": data.Title,
        "Authors": json.dumps(data.Authors),
        "Publisher": data.Publisher,
        "Published Date": data.Published_Date,
        "Description": data.Description,
        "ISBN 10": data.ISBN_10,
        "ISBN 13": data.ISBN_13,
        "Page Count": data.Page_Count,
        "Categories": json.dumps(data.Categories),
        "Language": data.Language,
        "Thumbnail URL": data.Thumbnail_URL,
        "Average Rating": data.Average_Rating or "None",
        "Ratings Count": data.Ratings_Count or "None",
        "Preview Link": data.Preview_Link or "None",
        "Info Link": data.Info_Link or "None",
        "isFavorite": str(data.isFavorite),
        "isCustomBook": str(True)  # always True when adding manually
    }

    prolog_data = {
        "Id": book_id,
        "Title": data.Title,
        "Authors": data.Authors,
        "Publisher": data.Publisher,
        "Published_Date": data.Published_Date,
        "Description": data.Description,
        "ISBN_10": data.ISBN_10,
        "ISBN_13": data.ISBN_13,
        "Page_Count": data.Page_Count,
        "Categories": data.Categories,
        "Language": data.Language,
        "Thumbnail_URL": data.Thumbnail_URL,
        "Average_Rating": data.Average_Rating or 0,
        "Ratings_Count": data.Ratings_Count or 0,
        "Preview_Link": data.Preview_Link,
        "Info_Link": data.Info_Link,
    }

    # Add to Prolog
    if not manager.create(prolog_data):
        raise HTTPException(status_code=500, detail="Failed to add book to Prolog database")

    # Save in Redis
    r.hset(key, mapping=redis_data)

    return Books(id=book_id, data=data)


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

# # 15. NLP Query
# @app.post("/nlp_query")
# def nlp_query(query: str):
#     result, book_ID = chatbot.run(query)
#     return {"result": result, "book_ID": book_ID}