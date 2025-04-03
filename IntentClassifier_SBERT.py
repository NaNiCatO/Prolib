from sentence_transformers import SentenceTransformer, util

class IntentClassifier:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load SBERT model
        self.model = SentenceTransformer(model_name)

        # Define standard query templates
        self.intent_templates = {
            "AUTHOR_INFO": [
                "Who wrote the book *Dune*?",
                "Tell me the author of *1984*.",
                "Who is the writer of *The Great Gatsby*?",
                "Which person wrote *Pride and Prejudice*?",
                "Find me the author of *Frankenstein*."
            ],
            "PUBLICATION_DATE": [
                "When was *Dune* published?",
                "What year was *1984* released?",
                "Tell me the publication date of *Brave New World*.",
                "What is the first edition date of *The Catcher in the Rye*?",
                "Give me the release year of *The Hobbit*."
            ],
            "BOOK_SUMMARY": [
                "Summarize the *Computer Aided Manufacturing*.",
                "Summarize the book *Dune*.",
                "Can you give me a summary of *1984*?",
                "Give me a short description of *Frankenstein*.",
                "What is *The Lord of the Rings* about?",
                "Tell me the plot of *To Kill a Mockingbird*."
            ],
            "BOOK_RECOMMENDATION": [
                "Recommend books similar to *Dune*.",
                "What books are like *1984*?",
                "Suggest some books if I liked *Brave New World*.",
                "Give me books that are similar to *The Hunger Games*.",
                "What are some alternatives to *Harry Potter*?"
            ],
            "BOOK_THEMES": [
                "What are the main themes in *Dune*?",
                "Tell me about the themes in *1984*.",
                "What are the philosophical ideas in *Brave New World*?",
                "Explain the central themes of *Frankenstein*.",
                "What moral lessons are in *To Kill a Mockingbird*?"
            ],
            "COMPARE_BOOKS": [
                "Compare *1984* and *Brave New World*.",
                "How is *Dune* different from *Foundation*?",
                "Which is better, *Lord of the Rings* or *Game of Thrones*?",
                "What are the similarities between *Harry Potter* and *Percy Jackson*?",
                "How do *Pride and Prejudice* and *Jane Eyre* compare?"
            ]
        }

        # Precompute embeddings
        self.template_embeddings = {
            category: self.model.encode(templates, convert_to_tensor=True)
            for category, templates in self.intent_templates.items()
        }

    def classify(self, user_input):
        user_embedding = self.model.encode(user_input, convert_to_tensor=True)

        best_match = None
        best_score = -1

        for category, embeddings in self.template_embeddings.items():
            scores = util.pytorch_cos_sim(user_embedding, embeddings)
            max_score = scores.max().item()

            if max_score > best_score:
                best_score = max_score
                best_match = category

        return best_match, best_score


# --- TESTING ---
if __name__ == "__main__":
    classifier = IntentClassifier()

    test_queries = [
        "Who wrote Dune?",
        "When was 1984 published?",
        "Summarize The Hobbit.",
        "Recommend books similar to Brave New World.",
        "What are the themes of Frankenstein?",
        "Compare 1984 and Brave New World."
    ]

    for query in test_queries:
        intent, score = classifier.classify(query)
        print(f"Query: {query}\n→ Intent: {intent} Score: {score:.4f}\n")
