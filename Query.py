from pyswip import Prolog
from SBERT import classify_intent

# Initialize Prolog engine
prolog = Prolog()
prolog.consult("data.pro")  # Load the Prolog knowledge base

def get_author_info(book_title):
    query = f"author('{book_title}', Author)."
    result = list(prolog.query(query))
    return result[0]['Author'] if result else "I don't know the author of that book."

def get_publication_date(book_title):
    query = f"published('{book_title}', Year)."
    result = list(prolog.query(query))
    return result[0]['Year'] if result else "I don't know when that book was published."

def get_book_summary(book_title):
    query = f"summary('{book_title}', Summary)."
    result = list(prolog.query(query))
    return result[0]['Summary'] if result else "I don't have a summary for that book."

def get_book_recommendations(book_title):
    query = f"recommend('{book_title}', Recommendation)."
    result = list(prolog.query(query))
    return result[0]['Recommendation'] if result else "I don't have recommendations for that book."

def get_book_themes(book_title):
    query = f"theme('{book_title}', Themes)."
    result = list(prolog.query(query))
    return result[0]['Themes'] if result else "I don't know the themes of that book."

# def compare_books(book1, book2):
#     query = f"compare_books('{book1}', '{book2}', Comparison)."
#     result = list(prolog.query(query))
#     return result[0]['Comparison'] if result else "I don't have a comparison for those books."

def extract_books(user_input):
    return "Find book name"

def handle_user_query(user_input):
    intent, score = classify_intent(user_input)
    book_titles = extract_books(user_input)
    
    # if intent == "COMPARE_BOOKS" and len(book_titles) == 2:
    #     return compare_books(book_titles[0], book_titles[1])
    
    if not book_titles:
        return "Sorry, I couldn't determine the book title. Can you rephrase?"
    
    book_title = book_titles[0]
    intent_handlers = {
        "AUTHOR_INFO": lambda: get_author_info(book_title),
        "PUBLICATION_DATE": lambda: get_publication_date(book_title),
        "BOOK_SUMMARY": lambda: get_book_summary(book_title),
        "BOOK_RECOMMENDATION": lambda: get_book_recommendations(book_title),
        "BOOK_THEMES": lambda: get_book_themes(book_title),
        # "COMPARE_BOOKS": lambda: "Provide two books for comparison (e.g., 'Compare Dune and Foundation').",
    }
    
    print(f"Intent: {intent}, Score: {score}")
    print(f"Extracted Book Titles: {book_titles}")
    
    return intent_handlers.get(intent, lambda: "Sorry, I don't understand that query.")()

if __name__ == "__main__":
    print("Welcome to the chatbot! Type 'exit' to quit.")
    
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        response = handle_user_query(user_query)
        print(f"Chatbot: {response}")
