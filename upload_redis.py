import redis
import uuid
import json
from pyswip import Prolog

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Connect to Prolog and consult the file
prolog = Prolog()
prolog.consult("books.pl")  # Your Prolog file with book facts

# Prolog term order:
# book(Title, Authors, Publisher, PublishedDate, Description, ISBN10, ISBN13,
#      PageCount, Categories, Language, Thumbnail, AvgRating, PeopleRated, PreviewLink, InfoLink)

# Read all books from Prolog
for result in prolog.query("book(Title, Authors, Publisher, PublishedDate, Description, ISBN10, ISBN13, PageCount, Categories, Language, Thumbnail, AvgRating, PeopleRated, PreviewLink, InfoLink)"):
    # Generate unique ID
    book_id = str(uuid.uuid4())
    redis_key = f"book:{book_id}"

    # Add 'Fav': False
    result["Fav"] = False

    # Convert list fields to JSON strings for Redis
    book_flat = {
    k: json.dumps([str(i, 'utf-8') if isinstance(i, bytes) else i for i in v]) if isinstance(v, list)
    else str(v, 'utf-8') if isinstance(v, bytes)
    else str(v)
    for k, v in result.items()
    }

    
    # Store in Redis
    r.hset(redis_key, mapping=book_flat)
    print(f"Uploaded book: {result['Title']} as {redis_key}")
