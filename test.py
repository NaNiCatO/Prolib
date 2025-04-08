import redis



r = redis.Redis(host="localhost", port=6379, decode_responses=True)



key = f"book:00bddaba-d7eb-4203-bfa1-f333b2875e71"
book = r.hgetall(key)
book_data = {
    "Title": "New Book",
    "Authors": ["Alice", "Bob"],
    "Publisher": "CoolPress",
    "Published Date": "2024",
    "Description": "Awesome read.",
    "ISBN 10": "0000000000",
    "ISBN 13": "9780000000000",
    "Page Count": 350,
    "Categories": ["Tech", "Programming"],
    "Language": "en",
    "Thumbnail URL": "http://example.com/thumb",
    "Average Rating": 4.8,
    "People Rated": 42,
    "Preview Link": "http://example.com/preview",
    "Info Link": "http://example.com/info"
}

boo
print(type(book))