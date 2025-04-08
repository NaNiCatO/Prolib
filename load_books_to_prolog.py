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

% Match by exact title (case-insensitive)
book_by_exact_title(Query, Book) :-
    downcase_atom(Query, LowerQuery),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    downcase_atom(Title, LowerTitle),
    LowerTitle = LowerQuery,
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

% Exact (case-insensitive) match by author name
book_by_exact_author(Query, Book) :-
    downcase_atom(Query, LowerQuery),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    member(Author, Authors),
    downcase_atom(Author, LowerAuthor),
    LowerAuthor = LowerQuery,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).

% Match by publisher (partial, case-insensitive)
book_by_publisher(Query, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    downcase_atom(Publisher, LowerPublisher),
    downcase_atom(Query, LowerQuery),
    contains_ignore_case(LowerPublisher, LowerQuery),
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).

% Exact (case-insensitive) match by publisher
book_by_exact_publisher(Query, Book) :-
    downcase_atom(Query, LowerQuery),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    downcase_atom(Publisher, LowerPublisher),
    LowerPublisher = LowerQuery,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).


% Query books by published date (full or year-only match)
book_by_pubdate(Query, Book) :-
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    (   downcase_atom(PubDate, LowerDate),
        downcase_atom(Query, LowerQuery),
        (   LowerDate = LowerQuery                  % exact full-date match
        ;   sub_string(LowerDate, 0, 4, _, LowerQuery)  % year match: first 4 chars
        )
    ),
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).


:- use_module(library(date)).  % needed for parse_time/2 and comparison

% Convert string to time stamp
safe_parse_date(String, Timestamp) :-
    catch(parse_time(String, iso_8601, Timestamp), _, fail).

% Find books published before a given date
book_before_date(Query, Book) :-
    safe_parse_date(Query, QueryTS),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    safe_parse_date(PubDate, BookTS),
    BookTS < QueryTS,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).

% Find books published after a given date
book_after_date(Query, Book) :-
    safe_parse_date(Query, QueryTS),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    safe_parse_date(PubDate, BookTS),
    BookTS > QueryTS,
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).


% Match if a query string occurs in title or author (NER fallback)
fallback_entity(Query, Book) :-
    book(Title, Authors, _, _, _, _, _, _, _, _, _, _, _, _, _),
    (contains_ignore_case(Title, Query) ;
     (member(Author, Authors), contains_ignore_case(Author, Query))),
    Book = book(Title, Authors, _, _, _, _, _, _, _, _, _, _, _, _, _).


% Exact (whole string) match for title or author, case-insensitive
fallback_exact_entity(Query, Book) :-
    downcase_atom(Query, LowerQuery),
    book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
         Categories, Lang, Thumb, Rating, RatingCount, Preview, Info),
    (   downcase_atom(Title, LowerTitle), LowerTitle = LowerQuery
    ;   member(Author, Authors),
        downcase_atom(Author, LowerAuthor),
        LowerAuthor = LowerQuery
    ),
    Book = book(Title, Authors, Publisher, PubDate, Desc, ISBN10, ISBN13, PageCount,
                Categories, Lang, Thumb, Rating, RatingCount, Preview, Info).



% Compute similarity score: category + author + rating
similarity_score(Cat1, Auth1, R1, Pub1, PC1, Lang1,
                 Cat2, Auth2, R2, Pub2, PC2, Lang2, Score) :-
    (intersects(Cat1, Cat2) -> S1 = 1 ; S1 = 0),
    (intersects(Auth1, Auth2) -> S2 = 1 ; S2 = 0),
    (number(R1), number(R2), R2 >= R1 -> S3 = 1 ; S3 = 0),
    (same_text(Pub1, Pub2) -> S4 = 1 ; S4 = 0),
    (number(PC1), number(PC2), abs(PC1 - PC2) =< 50 -> S5 = 1 ; S5 = 0),
    (same_text(Lang1, Lang2) -> S6 = 1 ; S6 = 0),
    Score is S1 + S2 + S3 + S4 + S5 + S6.



% True if two lists share any element (case-insensitive, optional)
intersects(List1, List2) :-
    member(X, List1),
    member(Y, List2),
    downcase_atom(X, X1),
    downcase_atom(Y, Y1),
    X1 = Y1,
    !.

% Case-insensitive atom comparison
same_text(A1, A2) :-
    downcase_atom(A1, L1),
    downcase_atom(A2, L2),
    L1 = L2.


% Recommend similar books with score ≥ 3
recommend_similar_books_with_score(
    book(Title1, Authors1, Publisher1, _, _, _, _, PageCount1, Categories1, Language1, _, Rating1, _, _, _),
    Score,
    book(Title2, Authors2, Publisher2, PubDate2, Desc2,
         ISBN10, ISBN13, PageCount2, Categories2, Language2,
         Thumb, Rating2, RatingCount, Preview, Info)
) :-
    book(Title2, Authors2, Publisher2, PubDate2, Desc2,
         ISBN10, ISBN13, PageCount2, Categories2, Language2,
         Thumb, Rating2, RatingCount, Preview, Info),

    normalize_space(atom(NT1), Title1),
    normalize_space(atom(NT2), Title2),
    NT1 \= NT2,

    similarity_score(Categories1, Authors1, Rating1, Publisher1, PageCount1, Language1,
                     Categories2, Authors2, Rating2, Publisher2, PageCount2, Language2, Score),

    Score >= 3.

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
