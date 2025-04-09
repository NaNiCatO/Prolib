from sentence_transformers import SentenceTransformer, util

class IntentClassifier:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load SBERT model
        self.model = SentenceTransformer(model_name)

        # Define standard query templates
        self.intent_templates = {
            "BOOK_TITLE": [
                "find a book wrote by Orson name Enchance published in 2005.",
                "What is the title of the book written by George Orwell about a dystopian future?",
                "Which book features a young girl named Scout growing up in the American South?",
                "Name the book that starts with 'Call me Ishmael.'",
                "What’s the novel where Frodo takes the One Ring to Mordor?",
                "Tell me the book that was written by Mary Shelley about a scientist who creates life.",
                "Which book is set on the desert planet Arrakis?",
                "What is the title of the novel that introduced Big Brother?",
                "Find the book by F. Scott Fitzgerald that critiques the American Dream.",
                "What book has the characters Elizabeth Bennet and Mr. Darcy?",
                "Which novel tells the story of a creature pieced together from corpses?",
                "Find a book wrote by Lisa published in 2021.",
                "give me a book name that worte by Thomas Cusick",
            ],
            "AUTHOR_INFO": [
                "Who wrote Dune?",
                "Who wrote 1984?",
                "Who wrote Frankenstein?",
                "Who wrote The Lord of the Rings?",
                "Who wrote To Kill a Mockingbird?",
                "Who wrote The Great Gatsby?",
                "Who wrote Speed Mathematics?",
                "Who wrote the book Dune?",
                "Tell me the author of 1984.",
                "Who is the writer of The Great Gatsby?",
                "Which person wrote Pride and Prejudice?",
                "Find me the author of Frankenstein.",
                "Who is the author of To Kill a Mockingbird?",
                "Name the writer of Moby Dick.",
                "Can you tell me who wrote Crime and Punishment?",
                "Who is behind the novel The Catcher in the Rye?",
                "Which author created Harry Potter?",
                "Tell me who penned The Hobbit.",
                "Who wrote the book Brave New World?",
                "Find the author of The Picture of Dorian Gray.",
                "Who’s the writer of Les Misérables?",
                "Who is the author of The Brothers Karamazov?",
                "Give me the name of the person who wrote Dracula.",
                "Who wrote One Hundred Years of Solitude?",
                "Who is the author of The Alchemist?",
                "Can you tell me the writer of The Road?",
                "Who is the author of The Chronicles of Narnia?"
            ],
            "PUBLICATION_DATE": [
                "When was Dune published?",
                "What year was 1984 released?",
                "When was 1984 published?",
                "When was Frankenstein published?",
                "When was The Lord of the Rings published?",
                "When was To Kill a Mockingbird published?",
                "When was The Great Gatsby published?",
                "Tell me the publication date of Brave New World.",
                "What is the first edition date of The Catcher in the Rye?",
                "Give me the release year of The Hobbit.",
                "When was Project Management published?",
                "What year did To Kill a Mockingbird come out?",
                "When did The Great Gatsby first get published?",
                "Tell me when Pride and Prejudice was originally released.",
                "What’s the publication year of Frankenstein?",
                "When was Moby Dick first published?",
                "Can you tell me when Crime and Punishment was published?",
                "Give me the release date of The Picture of Dorian Gray.",
                "When did Les Misérables come out?",
                "What year was The Brothers Karamazov published?",
                "When did Dracula first appear in print?",
                "Tell me the original publication date of One Hundred Years of Solitude.",
                "When was The Alchemist first published?",
                "What’s the publishing year of The Road?",
                "When did The Chronicles of Narnia start being published?"
            ],
            "BOOK_SUMMARY": [
                "Summarize the Computer Aided Manufacturing.",
                "Summarize the book Dune.",
                "Can you give me a summary of 1984?",
                "Give me a short description of Frankenstein.",
                "What is The Lord of the Rings about?",
                "Tell me the plot of To Kill a Mockingbird.",
                "Summarize Dishoom.",
                "Summarize The Hobbit.",
                "Summarize The Hunger Games.",
                "Summarize Harry Potter.",
                "Summarize Frankenstein.",
                "Summarize The Lord of the Rings.",
                "Summarize To Kill a Mockingbird.",
                "Summarize The Great Gatsby.",
                "Summarize Brave New World.",
                "Summarize The Catcher in the Rye.",
                "Summarize Moby Dick.",
                "Can you give me a summary of Quantum Enigma?",
                "What's the story of The Great Gatsby?",
                "Tell me what Brave New World is about.",
                "Give me a brief overview of The Catcher in the Rye.",
                "Can you explain the plot of Moby Dick?",
                "Summarize the narrative of Pride and Prejudice.",
                "What is Les Misérables about?",
                "Give a short summary of One Hundred Years of Solitude.",
                "Tell me the main storyline of The Alchemist.",
                "Summarize the content of The Road.",
                "What's the main idea of The Chronicles of Narnia?",
                "Can you describe the plot of The Picture of Dorian Gray?",
                "Summarize the main points of Crime and Punishment.",
                "Can you give me a summary of Dune?",
                "Can you give me a summary of 1984?",
                "Can you give me a summary of Frankenstein?",
                "Can you give me a summary of The Lord of the Rings?",
                "Can you give me a summary of To Kill a Mockingbird?",
                "Can you give me a summary of The Great Gatsby?",
                "Can you give me a summary of Brave New World?",
            ],
            "RATING": [
                "How many people rated Core Python Programming?"
                "What is the average rating of Dune?",
                "How many people rated 1984?",
                "Tell me the Goodreads rating for The Great Gatsby.",
                "What’s the average score for Pride and Prejudice?",
                "Give me the ratings count of Frankenstein.",
                "How well-rated is To Kill a Mockingbird?",
                "Can you show me how many ratings The Hobbit has?",
                "What’s the reader rating for The Catcher in the Rye?",
                "How popular is The Lord of the Rings based on ratings?",
                "I’d like to know the average review score of Brave New World.",
            ],
            "BOOK_RECOMMENDATION": [
                "Recommend books similar to *Dune*.",
                "What books are like *1984*?",
                "Suggest some books if I liked *Brave New World*.",
                "Give me books that are similar to *The Hunger Games*.",
                "What are some alternatives to *Harry Potter*?",
                "I loved *The Lord of the Rings*—what should I read next?",
                "Looking for books like *Ender’s Game*—any ideas?",
                "If I liked *The Catcher in the Rye*, what else might I enjoy?",
                "Recommend something for fans of *The Handmaid’s Tale*.",
                "Books like *The Name of the Wind*, please!",
                "What should I read if I enjoyed *Percy Jackson*?",
                "Can you suggest sci-fi novels with deep worldbuilding like *Dune*?",
                "Any fantasy series that feel like *A Song of Ice and Fire*?",
                "What are some dark dystopian novels like *1984* and *Fahrenheit 451*?",
                "Books for people who liked *Twilight* but want something a bit deeper.",
                "I want a mystery or thriller like *Gone Girl*. Any suggestions?",
                "What are some underrated fantasy books?",
                "Give me some cyberpunk books like *Neuromancer*.",
                "Suggest post-apocalyptic books similar to *The Road*.",
                "Books with similar themes to *To Kill a Mockingbird*?",
                "Are there any modern books like *Jane Eyre*?",
                "What should I read after finishing *Shadow and Bone*?",
                "Books with strong female leads like *Katniss Everdeen* or *Lyra Belacqua*?",
                "Can you recommend epic fantasy that isn’t too dense?",
                "What’s a good follow-up after reading *Slaughterhouse-Five*?",
                "Looking for coming-of-age stories like *Perks of Being a Wallflower*."
            ],
            "ADD_BOOK": [
                "Add a book to my collection.",
                "I want to add a book.",
                "Can you add a book for me?",
                "Please add a book.",
                "I need to add a book to my list.",
                "Add a new book.",
                "I want to include a book.",
                "Can you include a book for me?",
                "Please include a book.",
                "I need to include a book in my collection.",
                "Add a new title to my collection.",
                "I want to add a new title.",
                "Can you add a new title for me?",
            ],
            "EDIT_BOOK": [
                "Edit the details of The Great Gatsby.",
                "I want to edit To Kill a Mockingbird.",
                "Can you edit 1984 for me?",
                "Please edit Pride and Prejudice.",
                "I need to edit Moby Dick in my list.",
                "Edit the information of War and Peace.",
                "I want to change the details of The Catcher in the Rye.",
                "Can you change the details of Jane Eyre for me?",
                "Please change the details of Brave New World.",
                "I need to update the information of The Hobbit."
                "I want to edit Python.",
            ],
            "DELETE_BOOK": [
                "Delete Crime and Punishment from my collection.",
                "I want to remove The Odyssey.",
                "Can you delete The Brothers Karamazov for me?",
                "Please remove Great Expectations.",
                "I need to delete Fahrenheit 451 from my list.",
                "Remove Les Misérables from my collection.",
                "I want to get rid of Wuthering Heights.",
                "Can you remove Dracula for me?",
                "Please delete Anna Karenina.",
                "I need to eliminate The Picture of Dorian Gray from my collection.",
                "Delete Physical Biology",
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
        "Compare 1984 and Brave New World.",
        "I want to add a new book.",
        "Edit my book",
        "Delete my book",
    ]

    for query in test_queries:
        intent, score = classifier.classify(query)
        print(f"Query: {query}\n→ Intent: {intent} Score: {score:.4f}\n")
