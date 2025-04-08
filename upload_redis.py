import redis
import uuid
import json
from pyswip import Prolog
from Prolog_Controller import PrologBookManager

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def to_str(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value)

def to_json_list(value):
    return json.dumps([to_str(item) for item in value])

# STEP 1: Clear old book entries
def clear_existing_books(redis_conn, pattern="book:*"):
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_conn.scan(cursor=cursor, match=pattern, count=1000)
        if keys:
            redis_conn.delete(*keys)
    print("✅ All existing book:* keys cleared.")

clear_existing_books(r)

# STEP 2: Connect to Prolog
prolog = PrologBookManager("books.pl")
results = prolog.get_all_books()

# STEP 3: Read and Upload
for result in results:
    # Generate unique ID
    try:
        redis_key = f"book:{result["Id"]}"
    except KeyError:
        print(result)
        continue
    #remove 'Id' from result
    result.pop("Id", None)
    # Add 'isFavorite' and 'isCustomBook'
    result["isFavorite"] = False
    result["isCustomBook"] = False

    # Convert to flat dict for Redis
    book_flat = {
        k: to_json_list(v) if isinstance(v, list)
        else to_str(v)
        for k, v in result.items()
    }

    # Upload to Redis
    r.hset(redis_key, mapping=book_flat)
    print(f"📚 Uploaded book: {result['Title']} as {redis_key}")
