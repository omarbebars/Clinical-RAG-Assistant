import json
import chromadb
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------
# Configuration
JSON_FILE = "cases_database.json"
COLLECTION_NAME = "medical_cases"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
DB_PATH = "./cases_db"


# ------------------------------------------------------------------

def load_data(file_path):
    """Loads the case studies from the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} documents from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def main():
    documents = load_data(JSON_FILE)
    if not documents:
        return

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Embedding model loaded.")

    client = chromadb.PersistentClient(path=DB_PATH)

    # Delete the old collection if it exists (to prevent errors)
    try:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            print(f"Old collection '{COLLECTION_NAME}' found. Deleting.")
            client.delete_collection(name=COLLECTION_NAME)
    except Exception as e:
        print(f"Error deleting old collection: {e}")

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    print(f"Embedding {len(documents)} small chunks. This may take a moment...")

    # 4. Loop through, embed, and store each document
    for doc in documents:
        embedding = model.encode(doc['text']).tolist()


        collection.add(
            embeddings=[embedding],
            documents=[doc['text']],
            # We'll just use the first 50 chars as a "source" locator
            metadatas=[{"source": doc['text'][:50] + "..."}],
            ids=[doc['id']]
        )

    print(f"\n--- SUCCESS! ---")
    print(f"Successfully embedded and stored {collection.count()} SMALL chunks.")
    print("\n--- PHASE 2 COMPLETE (FIXED) ---")


if __name__ == "__main__":
    main()