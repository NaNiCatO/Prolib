from SBERT import classify_intent

def get_author_info():
    return "Author information retrieval is not implemented yet."

def get_publication_date():
    return "Publication date retrieval is not implemented yet."

def get_book_summary():
    return "Book summary retrieval is not implemented yet."

def get_book_recommendations():
    return "Book recommendations are not implemented yet."

def get_book_themes():
    return "Book theme analysis is not implemented yet."

def compare_books():
    return "Book comparison is not implemented yet."

def handle_user_query(user_input):
    intent, score = classify_intent(user_input)
    
    intent_handlers = {
        "AUTHOR_INFO": get_author_info,
        "PUBLICATION_DATE": get_publication_date,
        "BOOK_SUMMARY": get_book_summary,
        "BOOK_RECOMMENDATION": get_book_recommendations,
        "BOOK_THEMES": get_book_themes,
        "COMPARE_BOOKS": compare_books,
    }
    
    handler = intent_handlers.get(intent, lambda: "Sorry, I don't understand that query.")
    return handler()

if __name__ == "__main__":
    print("Welcome to the chatbot! Type 'exit' to quit.")
    
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        response = handle_user_query(user_query)
        print(f"Chatbot: {response}")
