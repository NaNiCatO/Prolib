from neo4j import GraphDatabase

# Connect to Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

def get_book_titles():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    titles = set()

    with driver.session() as session:
        result = session.run("MATCH (b:Book) RETURN b.title")
        for record in result:
            titles.add(record["b.title"].lower())  # Convert to lowercase

    driver.close()
    return titles

# Save to book_titles.txt
book_titles = get_book_titles()
with open("book_titles.txt", "w", encoding="utf-8") as f:
    for title in book_titles:
        f.write(title + "\n")

print(f"✅ Fetched {len(book_titles)} book titles from Neo4j.")
