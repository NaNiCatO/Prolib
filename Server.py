from fastapi import FastAPI, HTTPException, Body
from typing import Optional
from Prolog_Controller import PrologBookManager

app = FastAPI()
manager = PrologBookManager("books.pl")

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
