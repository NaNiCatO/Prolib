import spacy

nlp = spacy.load("en_core_web_sm")

# Your queries
queries = [
    "Who wrote Dune?",
    "When was 1984 published?",
    "Summarize The Hobbit.",
    "Recommend books similar to Brave New World.",
    "What are the themes of Frankenstein?",
    "Compare 1984 and Brave New World.",
]

for query in queries:
    doc = nlp(query)
    print(f"\nQuery: {query}")
    for ent in doc.ents:
        print(f" - {ent.text} ({ent.label_})")
