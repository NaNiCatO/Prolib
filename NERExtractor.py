import spacy

class BookNERExtractor:
    def __init__(self, model="en_core_web_trf"):
        self.nlp = spacy.load(model)

    def extract_ner_entities(self, text):
        doc = self.nlp(text)
        entities = [
            {"text": ent.text.strip(), "label": ent.label_}
            for ent in doc.ents
            if ent.label_ in {"WORK_OF_ART", "PERSON", "ORG", "DATE"}
        ]
        # print(f"Extracted NER entities: {entities}")
        return entities

    def extract_fallback_candidates(self, text):
        doc = self.nlp(text)
        candidates = set()

        for chunk in doc.noun_chunks:
            candidates.add(chunk.text.strip())

        tokens = [t.text for t in doc if t.is_alpha and not t.is_stop]
        for i in range(len(tokens)):
            candidates.add(tokens[i])
            if i < len(tokens) - 1:
                bigram = f"{tokens[i]} {tokens[i+1]}"
                candidates.add(bigram)

        return list(candidates)

    def extract_all(self, text):
        return {
            "ner_entities": self.extract_ner_entities(text),
            "fallback_candidates": self.extract_fallback_candidates(text)
        }

if __name__ == "__main__":
    extractor = BookNERExtractor()
    text = ["Find book wrote by Orson Scott Card name Enchantment published in 2005.",
        "Find a book wrote by Lisa Regan name Hush Little Girl published in 2021.",
        ]
    for t in text:
        print(f"\n🔍 Query: {t}")
        result = extractor.extract_all(t)
        # print(f"NER Entities: {result['ner_entities']}")
        print(f"Fallback Candidates: {result['fallback_candidates']}")

