from IntentClassifier_SBERT import IntentClassifier
from NERExtractor import BookNERExtractor
from Prolog_Controller import PrologBookManager
from Decoder import Decoder


def contains_digit(s):
    return any(c.isdigit() for c in s)

def extract_isbn(book):
    return book.get("ISBN 13") or book.get("ISBN 10")

def intersect_books_by_isbn(result_lists):
    non_empty_lists = [rl for rl in result_lists if rl]
    if not non_empty_lists:
        return []
    
    isbn_maps = []
    for result_list in non_empty_lists:
        isbn_map = {extract_isbn(book): book for book in result_list if extract_isbn(book)}
        isbn_maps.append(isbn_map)

    common_isbns = set(isbn_maps[0])
    for isbn_map in isbn_maps[1:]:
        common_isbns &= set(isbn_map)

    return [isbn_maps[0][isbn] for isbn in common_isbns]

def merge_books_by_isbn(result_lists):
    merged = {}
    for result_list in result_lists:
        for book in result_list:
            isbn = extract_isbn(book)
            if isbn and isbn not in merged:
                merged[isbn] = book
    return list(merged.values())



class NLPPipeline:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.ner_extractor = BookNERExtractor()
        self.prolog_controller = PrologBookManager()
        self.decoder = Decoder()

    def Query_Prolog_Knowledge_Base(self, query: str, spacy_entities: list, fallback_candidates: list):
        # Query Prolog Knowledge Base
        query_list_Spacy = [
            self.prolog_controller.query_by_exact_title,
            self.prolog_controller.query_by_author,
            self.prolog_controller.query_by_publisher,
            self.prolog_controller.query_by_publication_date,
        ]

        query_list_fallback = [
            self.prolog_controller.query_by_exact_title,
            self.prolog_controller.query_by_exact_author,
            self.prolog_controller.query_by_exact_publisher,
            self.prolog_controller.query_by_publication_date,
        ]

        all_result_lists = []

        # Step 1: Try spacy_entities
        for entity in spacy_entities:
            for query_func in query_list_Spacy:
                if entity["label"] == "DATE":
                    if query_func.__name__ == "query_by_publication_date":
                        #check entity in query if infront of entity["text"] is "after"
                        pos = query.find(entity["text"])
                        if pos != -1 and query[pos-6:pos-1] == "after":
                            result = self.prolog_controller.query_by_after_publication_date(entity["text"])
                            if result:
                                print(f"Hit: {entity['text']} ({'query_by_after_publication_date'})")
                                all_result_lists.append(result)
                        elif pos != -1 and query[pos-7:pos-1] == "before":
                            result = self.prolog_controller.query_by_before_publication_date(entity["text"])
                            if result:
                                print(f"Hit: {entity['text']} ({'query_by_before_publication_date'})")
                                all_result_lists.append(result)
                        else:
                            result = query_func(entity["text"])
                            if result:
                                print(f"Hit: {entity['text']} ({query_func.__name__})")
                                all_result_lists.append(result)
                else:
                    result = query_func(entity["text"])
                    if result:
                        print(f"Hit: {entity['text']} ({query_func.__name__})")
                        all_result_lists.append(result)

        # Step 2: If found, intersect results
        final_results = intersect_books_by_isbn(all_result_lists)

        # Step 3: If intersection is empty, fallback to candidates (no intersection, just merge)
        if not final_results:
            print("No results found in Prolog. Trying fallback candidates...")
            fallback_results = []
            sorted_fallback = sorted(fallback_candidates, key=len, reverse=True)
            
            for candidate in sorted_fallback:
                for query_func in query_list_fallback:
                    if contains_digit(candidate):
                        if query_func.__name__ == "query_by_publication_date":
                            #check entity in query if infront of entity["text"] is "after"
                            pos = query.find(candidate)
                            if pos != -1 and query[pos-6:pos-1] == "after":
                                result = self.prolog_controller.query_by_after_publication_date(candidate)
                                if result:
                                    print(f"Hit: {candidate} ({'query_by_after_publication_date'})")
                                    fallback_results.append(result)
                            elif pos != -1 and query[pos-7:pos-1] == "before":
                                result = self.prolog_controller.query_by_before_publication_date(candidate)
                                if result:
                                    print(f"Hit: {candidate} ({'query_by_before_publication_date'})")
                                    fallback_results.append(result)
                            else:
                                result = query_func(candidate)
                                if result:
                                    print(f"Hit: {candidate} ({query_func.__name__})")
                                    fallback_results.append(result)
                    else:
                        result = query_func(candidate)
                        if result:
                            print(f"Hit: {candidate} ({query_func.__name__})")
                            fallback_results.append(result)
            
            final_results = merge_books_by_isbn(fallback_results)

        return final_results

    def Intent_specific_result_retrieval_and_Generate_respons(self, intent: str, final_results: list):
        if intent == "BOOK_RECOMMENDATION":
            top_5_similar = self.prolog_controller.recommend_similar_books_sorted(final_results[0])
            response = f"Top 5 similar books with {final_results[0]['Title']}: \n- " + "- ".join([book['Title']+'\n' for book in top_5_similar])
            #top5 book ids
            book_ID = [book["Id"] for book in top_5_similar]
        else:
            # Step 4.1: Check if the intent is in the list of intents
            if intent == "BOOK_TITLE":
                result = final_results[0]["Title"]
                # print(f"Book Title: {result}")
            elif intent == "AUTHOR_INFO":
                result = final_results[0]["Authors"]
                # print(f"Author Info: {result}")
            elif intent == "PUBLICATION_DATE":
                result = final_results[0]["Published Date"]
                # print(f"Publication Date: {result}")
            elif intent == "BOOK_SUMMARY":
                result = final_results[0]["Description"]
                # print(f"Book Summary: {result}")
            elif intent == "RATING":
                print(final_results[0])
                result = f"Average Rating: {final_results[0]['Average Rating']}, Ratings Count: {final_results[0]['Ratings Count']}"
                # print(f"Rating: {result}")
            else:
                print("Unknown intent. No action taken.")
                return "Unknown intent. No action taken."
            book_name = final_results[0]["Title"]

            # Step 4.5: Convert result to string
            if isinstance(result, list):
                result = ", ".join([str(r) for r in result])
            elif isinstance(result, dict):
                result = ", ".join([f"{k}: {v}" for k, v in result.items()])
            elif isinstance(result, str):
                result = result.strip()
            else:
                result = str(result)
            # print(f"Result: {result}")

            # Step 5: Generate response using Decoder
            response = self.decoder.generate_response(query, result, intent, book_name)
            book_ID = final_results[0]["Id"]
        return response, book_ID

    def run(self, query: str):
        # Step 1: Intent Classification
        intent, score = self.intent_classifier.classify(query)
        print(f"[Intent] {intent}" + f" (Score: {score:.4f})")
        if score < 0.4:
            # print("Low confidence in intent classification.")
            return "Low confidence in intent classification."

        # Step 2: Named Entity Recognition
        ner_result = self.ner_extractor.extract_all(query)
        print(f"NER Result: {ner_result}")
        spacy_entities = ner_result["ner_entities"]
        # print(f"Spacy Entities: {spacy_entities}")
        fallback_candidates = ner_result["fallback_candidates"]
        # print(f"Fallback Candidates: {fallback_candidates}")
        
        # Step 3: Query Prolog Knowledge Base
        final_results = self.Query_Prolog_Knowledge_Base(query, spacy_entities, fallback_candidates)

        print(f"Books found: {len(final_results)}")
        # print(f"final_results: {final_results}")
        if not final_results:
            print("No relevant information found.")
            return "No relevant information found."

        # Step 4: Intent-specific result retrieval and response generation
        # print(intent)
        response = self.Intent_specific_result_retrieval_and_Generate_respons(intent, final_results)
        

        print(f"Query: {query}")
        # print(f"Response: {response}")
        return response


# --- TESTING ---
if __name__ == "__main__":
    pipeline = NLPPipeline()
    test_queries = [
        "give me a book name that worte by Sriram Pemmaraju",
        "Who wrote Python?",
        "When was Farewell to Reality published?",
        "Summarize Python.",
        "Can you give me a summary of Triad?",
        "Find book wrote by Orson Scott Card name Enchantment published in 2005.",
        "Find a book wrote by Lisa Regan and published in 2021.",
        "How many people rated Core Python Programming?",
        "Can you recommend some books that similar themes to Python?",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result, book_id = pipeline.run(query)
        print("_________")
        print(f"Result: {result}")
        print(f"Book ID: {book_id}")
        # # if result:
        #     print(f"Result: {len(result['result'])}")
        # else:
        #     print("No relevant information found.")
        # print(f"Result: {result}")