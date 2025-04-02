from transformers import AutoTokenizer
from pyswip import Prolog

# Initialize Prolog KB
prolog = Prolog()
book_titles = [
    "Dune",
    "1984",
    "The Hobbit",
    "Brave New World",
    "Frankenstein"
]
# Assert book facts
for title in book_titles:
    prolog.assertz(f'book("{title.lower()}")')

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Example queries
test_queries = [
    "Who wrote Dune?",
    "When was 1984 published?",
    "Summarize The Hobbit.",
    "Recommend books similar to Brave New World.",
    "What are the themes of Frankenstein?",
    "Compare 1984 and Brave New World.",
]

# Helper to check Prolog for books or authors
def check_book_or_author(tokens, prolog):
    matches = []
    for n in range(1, 4):  # n-gram size
        phrases = ''
        for i in range(len(tokens) - n + 1):
            if tokens[i].startswith("##"):
                phrases += tokens[i][2:]
            else:
                phrases += tokens[i] + " "
            phrase = phrases.strip().lower()
            print(f"Checking phrase: '{phrase}'")
            if list(prolog.query(f'book("{phrase}")')):
                matches.append((i, i+n, phrase, "book"))
    return matches

# Process each query
for query in test_queries:
    tokens = tokenizer.tokenize(query)
    matches = check_book_or_author(tokens, prolog)
    print(f"\nQuery: {query}")
    print(f"Tokens: {tokens}")
    print("Matches:")
    for match in matches:
        i, j, phrase, tag = match
        matched_text = " ".join(tokens[i:j])
        print(f"  - [{tag.upper()}] '{matched_text}' (tokens {i} to {j-1})")
