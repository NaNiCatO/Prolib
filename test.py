from transformers import pipeline
from IntentClassifier_SBERT import IntentClassifier

# Load a model for text generation
response_generator = pipeline("text2text-generation", model="google/flan-t5-large")

# Function to generate a human-like response
def generate_response(user_query, intent, data):
    prompt = (
        f"You are a helpful assistant answering user questions in a friendly, detailed way.\n\n"
        f"User Query: {user_query}\n"
        f"Intent: {intent}\n"
        f"Relevant Information: {data}\n\n"
        f"Now, write a natural and engaging response for the user:"
    )
    response = response_generator(prompt, max_length=1000)
    return response[0]['generated_text']

def get_intent(user_query):
    intent_classifier = IntentClassifier()
    intent, score = intent_classifier.classify(user_query)
    if score < 0.4:
        return "Unknown"
    return intent

# Example usage
user_query = "What is Python for Unix and Linux System Administration about?"
intent = get_intent(user_query)
data = "A guide to using the Python computer language to handle a variety of tasks in both the Unix and Linux servers. It covers the basics of Python programming and how to use it for system administration tasks."

print(generate_response(user_query, intent, data))
