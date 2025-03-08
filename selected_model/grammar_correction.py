from gramformer import Gramformer

# Load Grammar Correction Model
gf = Gramformer(models=1, use_gpu=False)  # Set use_gpu=True if you have a GPU

def fix_grammar(text):
    corrected_sentences = gf.correct(text, max_candidates=1)
    return list(corrected_sentences)[0] if corrected_sentences else text

# --- TESTING ---
if __name__ == "__main__":
    test_sentences = [
        "Who is write Dune?",
        "Give me book recommend for 1984?",
        "What is themes of Frankenstein?"
    ]

    for sentence in test_sentences:
        corrected_text = fix_grammar(sentence)
        print(f"Original: {sentence} → Fixed: {corrected_text}")
