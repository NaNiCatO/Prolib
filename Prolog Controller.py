from pyswip import Prolog

class PrologBookManager:
    def __init__(self, pl_file="books.pl"):
        self.prolog = Prolog()
        self.prolog.consult(pl_file)


    #___________________manipulate the Prolog knowledge base____________________
    def get_by_isbn(self, isbn13):
        query = f'book_by_isbn("{isbn13}", Book)'
        result = list(self.prolog.query(query))
        return result[0]['Book'] if result else None

    def remove_by_isbn(self, isbn13):
        book = self.get_by_isbn(isbn13)
        if not book:
            return False
        fact = self._term_to_fact_string(book)
        self.prolog.query(f"retract({fact})")  # ✅ use query instead of assertz
        return True

    def _term_to_fact_string(self, term):
        """Convert a pyswip compound term into a clean Prolog fact string."""
        if isinstance(term, bytes):
            return f'"{term.decode("utf-8")}"'
        elif isinstance(term, list):
            return "[" + ", ".join(self._term_to_fact_string(t) for t in term) + "]"
        elif isinstance(term, (int, float)):
            return str(term)
        elif isinstance(term, str):
            return f'"{term}"'
        elif isinstance(term, tuple):  # top-level book(...) tuple
            return "book(" + ", ".join(self._term_to_fact_string(t) for t in term) + ")"
        else:
            return "na"

    def create(self, book_dict):
        fact = "book(" + ", ".join(self._format_arg(v) for v in book_dict.values()) + ")"
        self.prolog.assertz(fact)

    def edit_by_isbn(self, isbn13, new_data):
        if self.remove_by_isbn(isbn13):
            self.create(new_data)
            return True
        return False

    def _format_arg(self, val):
        if isinstance(val, list):
            return "[" + ", ".join(self._format_arg(v) for v in val) + "]"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, str):
            return '"' + val.replace('"', '\\"') + '"'
        return "na"

    def _make_fact_string(self, book_term):
        # Converts SWI-Prolog compound term to string
        # book_term looks like: book('Title', ['Author'], ...)
        return str(book_term)
    
    #___________________query the Prolog knowledge base____________________
    def query_by_title(self, title_keyword):
        query = f'book_by_title("{title_keyword}", Book)'
        return self._collect_results(query)

    def query_by_author(self, author_keyword):
        query = f'book_by_author("{author_keyword}", Book)'
        return self._collect_results(query)

    def query_custom(self, filters: dict):
        # Example: filters = {"Title": "Deep", "Author": "Goodfellow"}
        conditions = []
        if "Title" in filters:
            conditions.append(f'contains_ignore_case(Title, "{filters["Title"]}")')
        if "Author" in filters:
            conditions.append(f'member(A, Authors), contains_ignore_case(A, "{filters["Author"]}")')
        if "Language" in filters:
            conditions.append(f'Lang = "{filters["Language"]}"')

        # Full query body
        query = (
            f'book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount, '
            f'Categories, Lang, Thumb, Rating, RatingCount, Preview, Info), ' +
            ", ".join(conditions) + ', ' +
            'Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount, '
            'Categories, Lang, Thumb, Rating, RatingCount, Preview, Info)'
        )
        return self._collect_results(query)

    def _collect_results(self, query):
        results = []
        for result in self.prolog.query(query):
            term = result["Book"]
            results.append(self._term_to_fact_string(term))
        return results



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
    "Ratings Count": 42,
    "Preview Link": "http://example.com/preview",
    "Info Link": "http://example.com/info"
}

pm = PrologBookManager("books.pl")

# Add book
pm.create(book_data)
print("Book added successfully.")

# Get book
book = pm.get_by_isbn("9780000000000")
print("Fetched Book:", book)

# Edit book
book_data["Title"] = "Updated Book Title"
pm.edit_by_isbn("9780000000000", book_data)

# Remove book
pm.remove_by_isbn("9780000000000")
print("Book removed successfully.")

# 🔍 Query by Title
books_about_ai = pm.query_by_title("Core Python Programming")
if books_about_ai:
    print("Book found")

# 🔍 Query by Author
books_by_knuth = pm.query_by_author("Wesley Chun")
if books_by_knuth:
    print("Book found")

# 🔍 Query by multiple fields
filtered = pm.query_custom({"Title": "Python in a Nutshell", "Author": "Alex Martelli"})

for book in filtered:
    print("Book found")