from IntentClassifier_SBERT import IntentClassifier
from NERExtractor import BookNERExtractor
from Prolog_Controller import PrologBookManager

class NLPPipeline:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.ner_extractor = BookNERExtractor()
        self.prolog_controller = PrologBookManager()

    def run(self, query: str):
        # Step 1: Intent Classification
        intent, score = self.intent_classifier.classify(query)
        print(f"[Intent] {intent}" +f" (Score: {score:.4f})")
        if score < 0.4:
            print("Low confidence in intent classification.")
            return None
        
        # Step 2: Named Entity Recognition
        ner_result = self.ner_extractor.extract_all(query)
        spacy_entities = ner_result["ner_entities"]
        print(f"Spacy Entities: {spacy_entities}")
        fallback_candidates = ner_result["fallback_candidates"]
        print(f"Fallback Candidates: {fallback_candidates}")

        # Step 3: Prolog Query
        found = False

        for ent in spacy_entities:
            result = self.prolog_controller.query_by_title(ent)
            if result:
                print(f"Found in KG: {result[0]}")
                found = True
                break
            else:
                print(f"Not found in KG → trying Prolog fallback for: {ent}")
                fallback = self.prolog_controller._collect_results(f'fallback_exact_entity("{ent}", Book)')
                if fallback:
                    print(f"Fallback matched: {fallback[0]}")
                    found = True
                    break
        if not found:
            print("Spacy missed or all entities failed. Falling back to chunks...")
            for chunk in fallback_candidates:
                fallback = self.prolog_controller._collect_results(f'fallback_exact_entity("{chunk}", Book)')
                if fallback:
                    print(f"Chunk matched: '{chunk}' → {fallback[0]}")
                    found = True
                    break
        if not found:
            print("No matches found in KG or fallback.")
            return None


        
        return {
            "result": result if len(result) != 0 else fallback,
            
        }


# --- TESTING ---
if __name__ == "__main__":
    pipeline = NLPPipeline()
    test_queries = [
        "Who wrote World Encyclopedia of Entrepreneurship?",
        "When was Farewell to Reality published?",
        "Summarize The Python.",
        "Recommend books similar to Brave New World.",
        "What are the themes of Frankenstein?",
        "Compare 1984 and Brave New World.",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = pipeline.run(query)
        print("_________")
        if result:
            print(f"Result: {len(result["result"])}")
        else:
            print("No relevant information found.")
#         print(f"Result: {result}")