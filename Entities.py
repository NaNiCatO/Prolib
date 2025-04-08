import spacy
from Prolog_Controller import PrologBookManager

pm = PrologBookManager("books.pl")
nlp = spacy.load("en_core_web_sm")

queries = [
    "Who wrote World Encyclopedia of Entrepreneurship?",
    "When was 1984 published?",
    "Summarize The Python.",
    "Recommend books similar to Brave New World.",
    "What are the themes of Frankenstein?",
    "Compare 1984 and Brave New World.",
]

def extract_candidates(text):
    doc = nlp(text)
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

for query in queries:
    print(f"\n🔍 Query: {query}")
    doc = nlp(query)
    ents = [ent.text.strip() for ent in doc.ents if ent.label_ in {"WORK_OF_ART", "PERSON", "ORG"}]

    found = False

    if ents:
        print(f"  ✅ spaCy entities: {ents}")
        for ent in ents:
            result = pm.query_by_title(ent)
            if result:
                print(f"    ✅ Found in KG: {result[0]}")
                found = True
            else:
                print(f"    ❌ Not found in KG → trying Prolog fallback for: {ent}")
                fallback = pm._collect_results(f'fallback_entity("{ent}", Book)')
                if fallback:
                    print(f"       ✅ Fallback matched: {fallback[0]}")
                    found = True

    if not ents or not found:
        print("  ⚠️ spaCy missed or all entities failed. Falling back to chunks...")
        for chunk in extract_candidates(query):
            fallback = pm._collect_results(f'fallback_entity("{chunk}", Book)')
            if fallback:
                print(f"    ✅ Chunk matched: '{chunk}' → {fallback[0]}")
                found = True
                break

    if not found:
        print("  ❌ No matches found at all.")
