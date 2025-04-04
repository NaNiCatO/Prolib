from IntentClassifier_SBERT import IntentClassifier
from NERExtractor import BookNERExtractor
from Prolog_Controller import PrologBookManager
from Decoder import Decoder

class NLPPipeline:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.ner_extractor = BookNERExtractor()
        self.prolog_controller = PrologBookManager()
        self.decoder = Decoder()

    def run(self, query: str):
        # Step 1: Intent Classification
        intent, score = self.intent_classifier.classify(query)
        # print(f"[Intent] {intent}" + f" (Score: {score:.4f})")
        if score < 0.4:
            # print("Low confidence in intent classification.")
            return None

        # Step 2: Named Entity Recognition
        ner_result = self.ner_extractor.extract_all(query)
        print(f"NER Result: {ner_result}")
        spacy_entities = ner_result["ner_entities"]
        print(f"Spacy Entities: {spacy_entities}")
        fallback_candidates = ner_result["fallback_candidates"]
        print(f"Fallback Candidates: {fallback_candidates}")
        
        #  Step 3: Query Prolog Knowledge Base
        query_list = [
            self.prolog_controller.query_by_title,
            self.prolog_controller.query_by_author,
            self.prolog_controller.query_by_publisher
        ]

        result = None
        book_name = None

        # Try all 3 functions for each entity in spacy_entities
        for entity in spacy_entities:
            for query_func in query_list:
                result = query_func(entity["text"])
                if result:
                    book_name = entity["text"]
                    break
            if result:
                break  # Exit the outer loop if result is found

        # If not found, do the same for fallback candidates
        if not result:
            for candidate in fallback_candidates:
                for query_func in query_list:
                    result = query_func(candidate)
                    if result:
                        book_name = candidate
                        break
                if result:
                    break

        
        
        # Step 4: Intent-specific result retrieval
        # print(intent)
        if intent == "AUTHOR_INFO":
            result = result[0]["Authors"]
            # print(f"Author Info: {result}")
        elif intent == "PUBLICATION_DATE":
            result = result[0]["Published Date"]
            # print(f"Publication Date: {result}")
        elif intent == "BOOK_SUMMARY":
            result = result[0]["Description"]
            # print(f"Book Summary: {result}")
        else:
            print("Unknown intent. No action taken.")
            return None
        

        # Step 4.5: Convert result to string
        if isinstance(result, list):
            result = ", ".join([str(r) for r in result])
        elif isinstance(result, dict):
            result = ", ".join([f"{k}: {v}" for k, v in result.items()])
        elif isinstance(result, str):
            result = result.strip()
        else:
            result = str(result)
        # print(f"Final Result: {result}")

        # Step 5: Generate response using Decoder
        response = self.decoder.generate_response(query, result, intent, book_name)
        print(f"Query: {query}")
        print(f"data: {result}")
        # print(f"Response: {response}")
        return response

# --- TESTING ---
if __name__ == "__main__":
    pipeline = NLPPipeline()
    test_queries = [
        # "When was Farewell to Reality published?",
        # "Summarize Python.",
        # "Who wrote Python?",
        # "Can you give me a summary of Triad?",
        "Find book wrote by Orson Scott Card name Enchantment published in 2005.",
        "Find a book wrote by Lisa Regan name Hush Little Girl published in 2021.",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = pipeline.run(query)
        print("_________")
        print(f"Result: {result}")
        # # if result:
        #     print(f"Result: {len(result['result'])}")
        # else:
        #     print("No relevant information found.")
        # print(f"Result: {result}")