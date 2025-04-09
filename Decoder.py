from transformers import pipeline
from IntentClassifier_SBERT import IntentClassifier

# Load pipelines
response_generator = pipeline("text2text-generation", model="google/flan-t5-large")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class Decoder:
    def __init__(self):
        self.need_summary = []

    @staticmethod
    def summarize_if_needed(data, max_chars=1000):
        if len(data) > max_chars:
            summarized = summarizer(data, max_length=200, min_length=50, do_sample=False)
            return summarized[0]['summary_text']
        
        return data

    @staticmethod
    def generate_response(user_query, data, intent, book_title="The book"):
        data = Decoder.summarize_if_needed(data)
        print(f"Data: {data}")

        prompt = (
            f"Q: {user_query} \n"
            f"Q: {user_query} Provided Data : \n\n {data} \n"
            f"Q: {user_query} Provided Data : \n\n {data} \nAnswer the question with the provided data \n"
            f"Generate a summary of the provided data.  \n\n"
        )

        response = response_generator(prompt, max_length=5000)
        return response[0]['generated_text']

if __name__ == "__main__":
    # test_generate_response()
    # Example usage
    user_query = "What is Python for Unix and Linux System Administration about?"
    intent = "BOOK_SUMMARY"
    data = "A guide to using the Python computer language to handle a variety of tasks in both the Unix and Linux servers. It covers the basics of Python programming and how to use it for system administration tasks."

    print(Decoder.generate_response(user_query, intent, data))
