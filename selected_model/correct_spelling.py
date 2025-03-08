from symspellpy import SymSpell, Verbosity
import pkg_resources

# Load SymSpell dictionary
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Load book titles from file
BOOK_TITLES = set()
with open("book_titles.txt", "r", encoding="utf-8") as f:
    for line in f:
        BOOK_TITLES.add(line.strip().lower())  # Convert to lowercase for matching

def correct_spelling(text):
    words = text.split()  # Split sentence into words
    corrected_words = []

    for word in words:
        # If the word is a book title, keep it as is
        if word.lower() in BOOK_TITLES:
            corrected_words.append(word)
        else:
            # Otherwise, apply spell correction
            suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
            corrected_words.append(suggestions[0].term if suggestions else word)

    return " ".join(corrected_words)

# --- TESTING ---
if __name__ == "__main__":
    test_sentences = [
        "Who is the authr of Dune?",
        "Recomend me a book like 1984",
        "Summarize Frankenstien",
        "Tell me about the lord of the rings"
    ]

    for sentence in test_sentences:
        corrected_text = correct_spelling(sentence)
        print(f"Original: {sentence} → Fixed: {corrected_text}")
