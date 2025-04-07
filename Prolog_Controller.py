from pyswip import Prolog
import ast

class PrologBookManager:
    def __init__(self, pl_file="books.pl"):
        self.prolog = Prolog()
        self.prolog.consult(pl_file)


    def _term_string_to_dict(self, term_str):
        if not term_str.startswith("book(") or not term_str.endswith(")"):
            return {}

        args_str = term_str[5:-1]

        try:
            parsed = ast.literal_eval(f"({args_str})")
        except Exception as e:
            print("Failed to parse term:", e)
            return {}

        if not isinstance(parsed, tuple) or len(parsed) != 15:
            return {}

        # Helper to decode bytes or keep value
        def decode(val):
            if isinstance(val, bytes):
                return val.decode("utf-8")
            elif isinstance(val, list):
                return [decode(v) for v in val]
            else:
                return val

        return {
            "Title": decode(parsed[0]),
            "Authors": decode(parsed[1]),
            "Publisher": decode(parsed[2]),
            "Published Date": decode(parsed[3]),
            "Description": decode(parsed[4]),
            "ISBN 10": decode(parsed[5]),
            "ISBN 13": decode(parsed[6]),
            "Page Count": decode(parsed[7]),
            "Categories": decode(parsed[8]),
            "Language": decode(parsed[9]),
            "Thumbnail URL": decode(parsed[10]),
            "Average Rating": decode(parsed[11]),
            "Ratings Count": decode(parsed[12]),
            "Preview Link": decode(parsed[13]),
            "Info Link": decode(parsed[14])
        }

    #___________________manipulate the Prolog knowledge base____________________
    def get_by_isbn(self, isbn13):
        query = f'book_by_isbn("{isbn13}", Book)'
        result = list(self.prolog.query(query))
        return self._term_string_to_dict(result[0]['Book']) if result else None


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
        # return status
        try:
            self.prolog.assertz(fact)  # ✅ use assertz to add the fact
            return True
        except Exception as e:
            print("Failed to add book:", e)
            return False

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
    def query_by_exact_title(self, title_keyword):
        query = f'book_by_exact_title("{title_keyword}", Book)'
        return self._collect_results(query)

    def query_by_title(self, title_keyword):
        query = f'book_by_title("{title_keyword}", Book)'
        return self._collect_results(query)
    
    def query_by_exact_author(self, author_keyword):
        query = f'book_by_exact_author("{author_keyword}", Book)'
        return self._collect_results(query)

    def query_by_author(self, author_keyword):
        query = f'book_by_author("{author_keyword}", Book)'
        return self._collect_results(query)
    
    def query_by_exact_publisher(self, publisher_keyword):
        query = f'book_by_exact_publisher("{publisher_keyword}", Book)'
        return self._collect_results(query)

    def query_by_publisher(self, publisher_keyword):
        query = f'book_by_publisher("{publisher_keyword}", Book)'
        return self._collect_results(query)
    
    def query_by_publication_date(self, pub_date_keyword):
        # reformat to YYYY-MM-DD
        pub_date_keyword = pub_date_keyword.replace(".", "-").replace("/", "-")
        query = f'book_by_pubdate("{pub_date_keyword}", Book)'
        return self._collect_results(query)
    
    def query_by_before_publication_date(self, pub_date_keyword):
        # reformat to YYYY-MM-DD
        if len(pub_date_keyword) == 4:
            pub_date_keyword += "-01-01"
        elif len(pub_date_keyword) == 7:
            pub_date_keyword += "-01"
        elif len(pub_date_keyword) == 10:
            pass
        pub_date_keyword = pub_date_keyword.replace(".", "-").replace("/", "-")
        full_date = pub_date_keyword
        year = pub_date_keyword[:4]
        # query full_date and year
        query = f'book_before_date("{full_date}", Book)'
        query2 = f'book_before_date("{year}", Book)'
        # combine results
        results = self._collect_results(query) + self._collect_results(query2)
        # remove duplicates
        unique_results = {self._make_fact_string(book): book for book in results}
        results = list(unique_results.values())
        return results

    
    def query_by_after_publication_date(self, pub_date_keyword):
        # reformat to YYYY-MM-DD and handle year-only cases
        if len(pub_date_keyword) == 4:
            pub_date_keyword += "-01-01"
        elif len(pub_date_keyword) == 7:
            pub_date_keyword += "-01"
        elif len(pub_date_keyword) == 10:
            pass
        pub_date_keyword = pub_date_keyword.replace(".", "-").replace("/", "-")
        full_date = pub_date_keyword
        year = pub_date_keyword[:4]
        # query full_date and year
        query = f'book_after_date("{full_date}", Book)'
        query2 = f'book_after_date("{year}", Book)'
        # combine results
        results = self._collect_results(query) + self._collect_results(query2)
        # remove duplicates
        unique_results = {self._make_fact_string(book): book for book in results}
        results = list(unique_results.values())
        return results

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
    

    def recommend_similar_books_sorted(self, reference_book, limit=5):
        # Use _format_arg to safely format each field
        args = [self._format_arg(reference_book[key]) for key in reference_book]
        book_term = f"book({', '.join(args)})"
        
        query = f'recommend_similar_books_with_score({book_term}, Score, Book)'

        results = []
        for result in self.prolog.query(query):
            book = self._term_string_to_dict(result["Book"])
            score = result["Score"]
            results.append((score, book))

        results.sort(key=lambda x: -x[0])  # Sort by descending similarity score
        return [book for score, book in results[:limit]]


    
    def _collect_results(self, query):
        results = []
        for result in self.prolog.query(query):
            book = self._term_string_to_dict(result["Book"])
            results.append(book)
        return results


    


if __name__ == "__main__":
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
    books_about_ai = pm.query_by_title("Triad")
    if books_about_ai:
        # print amount of books found
        print(f"Found {len(books_about_ai)} books")
    else :
        print("No books found")

    # 🔍 Query by Author
    books_by_knuth = pm.query_by_author("Wesley Chun")
    if books_by_knuth:
        print(f"Found {len(books_by_knuth)} books by the author")
    
    # 🔍 Query by Publisher
    books_by_publisher = pm.query_by_publisher("Prentice Hall Professional")
    if books_by_publisher:
        print(f"Found {len(books_by_publisher)} books by the publisher")

    # 🔍 Query by multiple fields
    filtered = pm.query_custom({"Title": "Python in a Nutshell", "Author": "Alex Martelli"})

    for book in filtered:
        print("Book found")

    books_by_pubdate = pm.query_by_publication_date("2023")
    if books_by_pubdate:
        print(f"Found {len(books_by_pubdate)} books published in 2023")

    books_before_2020 = pm.query_by_after_publication_date("2020-01-01")
    if books_before_2020:
        print(f"Found {len(books_before_2020)} books published before 2020")


    book = pm.get_by_isbn("9781449379322")
    top_5_similar = pm.recommend_similar_books_sorted(book)
    for b in top_5_similar:
        print("Recommended:", b["Title"])
