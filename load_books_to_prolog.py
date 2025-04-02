import csv
import os

genres = ["python", "fantasy", "mystery", "science fiction", "romance", "history",
          "Biology", "Chemistry", "Mathematics", "Physics", "Programming", "Cooking",
          "Cookbooks", "Mental Health", "Exercise", "Nutrition", "Self-help", "Management",
          "Entrepreneurship", "Business Economics", "Business Success", "Finance"]

def sanitize(value):
    if not value or value.strip() == "":
        return "na"
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'

def sanitize_list(value):
    if not value or value.strip().lower() == "n/a":
        return "[]"
    try:
        items = [item.strip() for item in value.split(",") if item.strip()]
        return "[" + ", ".join(sanitize(item) for item in items) + "]"
    except Exception:
        return "[]"

def sanitize_number(value):
    try:
        return str(int(float(value)))
    except:
        return "na"

def is_valid_book(row, min_pages=50, require_rating=True, language="en"):
    if not row["Title"].strip() or not row["Authors"].strip():
        return False
    if require_rating and not row["Average Rating"].replace('.', '', 1).isdigit():
        return False
    if row["ISBN 10"].strip() == "N/A" and row["ISBN 13"].strip() == "N/A":
        return False
    return True

def csv_to_prolog(csv_filename, plfile, skiplog):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not is_valid_book(row):
                skiplog.write(f"Skipped: {row.get('Title', 'Unknown')} in {csv_filename}\n")
                continue

            fact = f"book({sanitize(row['Title'])}, " \
                   f"{sanitize_list(row['Authors'])}, " \
                   f"{sanitize(row['Publisher'])}, " \
                   f"{sanitize(row['Published Date'])}, " \
                   f"{sanitize(row['Description'])}, " \
                   f"{sanitize(row['ISBN 10'])}, " \
                   f"{sanitize(row['ISBN 13'])}, " \
                   f"{sanitize_number(row['Page Count'])}, " \
                   f"{sanitize_list(row['Categories'])}, " \
                   f"{sanitize(row['Language'])}, " \
                   f"{sanitize(row['Thumbnail URL'])}, " \
                   f"{sanitize_number(row['Average Rating'])}, " \
                   f"{sanitize_number(row['Ratings Count'])}, " \
                   f"{sanitize(row['Preview Link'])}, " \
                   f"{sanitize(row['Info Link'])}).\n"
            plfile.write(fact)

def add_helper_rules(plfile):
    plfile.write(
        """
% Find a book by title
book_by_title(Title, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
        Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    Title = Title,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).
\n""")
def add_helper_rules(plfile):
    plfile.write(
        """
% Find a book by ISBN-13
book_by_isbn(ISBN, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    ISBN13 = ISBN,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).
        
% Case-insensitive substring match (naive)
contains_ignore_case(Haystack, Needle) :-
    downcase_atom(Haystack, LowerHaystack),
    downcase_atom(Needle, LowerNeedle),
    sub_string(LowerHaystack, _, _, _, LowerNeedle).

% Match by title (partial, case-insensitive)
book_by_title(Query, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    contains_ignore_case(Title, Query),
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).

% Match by author (partial, case-insensitive)
book_by_author(Query, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    member(Author, Authors),
    contains_ignore_case(Author, Query),
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).
\n"""
    )





# Write to a single .pl file
with open("books.pl", "w", encoding="utf-8") as plfile, open("skipped_books.log", "w", encoding="utf-8") as skiplog:
    plfile.write(":- dynamic(book/15).\n\n")
    add_helper_rules(plfile)
    for genre in genres:
        csv_file = f"test_data/{genre}_books.csv"
        if os.path.exists(csv_file):
            print(f"Processing: {csv_file}")
            csv_to_prolog(csv_file, plfile, skiplog)
        else:
            print(f"Missing: {csv_file}")
