from transformers import pipeline
from IntentClassifier_SBERT import IntentClassifier

# Load a model for text generation
response_generator = pipeline("text2text-generation", model="google/flan-t5-large")

class Decoder:
    def __init__(self):
        self.need_summary = []

    @staticmethod
    def generate_response(user_query, data, intent, book_title):
        # Doesnt need summary
        if intent in ["AUTHOR_INFO", "PUBLICATION_DATE"]:
            prompt = (
                f"Q: {user_query} A:\n"
                f"Q: {user_query} Provided Data : \n\n {data} A:\n"
                f"Q: {user_query} Provided Data : \n\n {data} \nAnswer the question with the provided data A:\n"
                f"Generate a summary of the provided data.  \n\n"
            )
        # Needs summary
        else:
            prompt = (
                f"Q: {user_query} A:{book_title} is about\n"
                f"Q: {user_query} Provided Data : \n\n {data} A:{book_title} is about\n"
                f"Q: {user_query} Provided Data : \n\n {data} \nAnswer the question with the provided data A:{book_title} is about\n"
                f"Generate a summary of the provided data.  \n\n"
            )
        
        response = response_generator(prompt, max_length=5000)
        return response[0]['generated_text']



    @staticmethod
    def get_intent(user_query):
        intent_classifier = IntentClassifier()
        intent, score = intent_classifier.classify(user_query)
        if score < 0.4:
            return "Unknown"
        return intent

    # def test_generate_response():
    #     test_cases = {
    #         "AUTHOR_INFO": [
    #             ("Who wrote the book Dune?", "Frank Herbert"),
    #             ("Tell me the author of 1984.", "George Orwell"),
    #             ("Who is the writer of Good Omens?", "Neil Gaiman, Terry Pratchett"),
    #         ],
    #         "PUBLICATION_DATE": [
    #             ("When was Dune published?", "1965"),
    #             ("What year was 1984 released?", "1949"),
    #             ("Give me the release year of The Hobbit.", "1937"),
    #         ],
    #         "BOOK_SUMMARY": [
    #             ("Summarize Dune.", "Dune follows Paul Atreides as he navigates political intrigue and war on the desert planet Arrakis, where spice is the most valuable resource."),
    #             ("Can you give me a summary of 1984?", "1984 is a dystopian novel set in a totalitarian society ruled by Big Brother, exploring themes of surveillance and government control."),
    #         ],
    #         "BOOK_RECOMMENDATION": [
    #             ("Recommend books similar to Dune.", "If you enjoyed Dune, you might like Foundation by Isaac Asimov or Hyperion by Dan Simmons, both of which explore complex sci-fi worlds."),
    #             ("What books are like 1984?", "If you liked 1984, consider reading Brave New World by Aldous Huxley or Fahrenheit 451 by Ray Bradbury, which explore similar dystopian themes."),
    #         ],
    #         "BOOK_THEMES": [
    #             ("What are the main themes in Dune?", "Dune explores themes of power, religion, ecology, and human resilience in an interstellar empire."),
    #             ("Tell me about the themes in 1984.", "1984 deals with themes of government surveillance, propaganda, totalitarianism, and the manipulation of truth."),
    #         ],
    #         "COMPARE_BOOKS": [
    #             ("Compare 1984 and Brave New World.", "1984 presents a society controlled by oppression and surveillance, while Brave New World depicts a dystopia where control is maintained through pleasure and conditioning."),
    #             ("Which is better, Lord of the Rings or Game of Thrones?", "The Lord of the Rings follows a classic good vs. evil narrative, while Game of Thrones presents morally ambiguous characters and political intrigue."),
    #         ]
    #     }

    #     for intent, queries in test_cases.items():
    #         for user_query, expected_intent, data in queries:
    #             response = generate_response(user_query, expected_intent, data)
    #             print(f"Query: {user_query}\nIntent: {expected_intent}\nResponse: {response}\n")

if __name__ == "__main__":
    # test_generate_response()
    # Example usage
    user_query = "What is Python for Unix and Linux System Administration about?"
    intent = Decoder.get_intent(user_query)
    data = "A guide to using the Python computer language to handle a variety of tasks in both the Unix and Linux servers. It covers the basics of Python programming and how to use it for system administration tasks."

    print(Decoder.generate_response(user_query, intent, data))
