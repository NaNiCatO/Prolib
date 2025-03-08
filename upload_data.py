# Description: This script reads CSV files from a folder and uploads the data to Neo4j and Redis.
import os
import glob
import pandas as pd
from neo4j import GraphDatabase
import redis
from tqdm import tqdm

# --- CONFIGURATION --- #
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Change this to your Neo4j password

REDIS_HOST = "localhost"
REDIS_PORT = 6379

DATA_FOLDER = "test_data/"  # Folder where CSV files are stored

# --- CONNECT TO DATABASES --- #
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# --- FUNCTION TO UPLOAD TO NEO4J --- #
def create_book(tx, title, authors, publisher, categories):
    query = """
    MERGE (b:Book {title: $title})
    SET b.publisher = $publisher
    FOREACH (cat IN $categories |
        MERGE (c:Category {name: cat})
        MERGE (b)-[:BELONGS_TO]->(c)
    )
    FOREACH (auth IN $authors |
        MERGE (a:Author {name: auth})
        MERGE (b)-[:WROTE_BY]->(a)
    )
    """
    tx.run(query, title=title, authors=authors, publisher=publisher, categories=categories)

# --- PROCESS ALL CSV FILES IN FOLDER --- #
csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))

for file in csv_files:
    print(f"Processing file: {file} ...")
    
    # Load CSV
    df = pd.read_csv(file)
    
    # Drop rows with missing titles
    df = df.dropna(subset=["Title"])

    # Upload to Neo4j
    print("Uploading data to Neo4j...")
    with neo4j_driver.session() as session:
        for _, row in tqdm(df.iterrows(), total=len(df)):
            title = str(row["Title"]).strip()  # Convert to string and remove extra spaces
            if title == "nan" or title == "":  # Skip invalid titles
                continue
            
            authors = row["Authors"].split(", ") if pd.notna(row["Authors"]) else []
            publisher = row["Publisher"] if pd.notna(row["Publisher"]) else "Unknown"
            categories = row["Categories"].split(", ") if pd.notna(row["Categories"]) else []
            
            session.write_transaction(create_book, title, authors, publisher, categories)

    print("Neo4j Upload Completed ✅")

    # Upload to Redis
    print("Uploading data to Redis...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        title = str(row["Title"]).strip()
        if title == "nan" or title == "":
            continue
        
        book_key = f"book:{title}"
        redis_client.hmset(book_key, {
            "description": row["Description"] if pd.notna(row["Description"]) else "No description",
            "rating": row["Average Rating"] if pd.notna(row["Average Rating"]) else "N/A",
            "page_count": row["Page Count"] if pd.notna(row["Page Count"]) else "Unknown",
            "isbn_10": row["ISBN 10"] if pd.notna(row["ISBN 10"]) else "N/A",
            "isbn_13": row["ISBN 13"] if pd.notna(row["ISBN 13"]) else "N/A",
            "preview_link": row["Preview Link"] if pd.notna(row["Preview Link"]) else "N/A",
            "thumbnail_url": row["Thumbnail URL"] if pd.notna(row["Thumbnail URL"]) else "N/A",
        })

    print(f"Redis Upload Completed ✅ for file: {file}\n")

# Close Neo4j Connection
neo4j_driver.close()
print("🎉 All files processed successfully!")
