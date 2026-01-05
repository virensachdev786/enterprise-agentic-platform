import json
import chromadb
from pathlib import Path

# Constants for Paths
BASE_DIR = Path("/Users/virensachdev/Desktop/enterprise-agentic-platform")
JSONL_PATH = BASE_DIR / "db/vectorstore/procedure_chunks.jsonl"

# Chroma Config
CHROMA_HOST = "localhost"
CHROMA_PORT = 8050
TENANT = "default_tenant"
DATABASE = "default_database"
COLLECTION_NAME = "procedures_kb"

def load_from_jsonl(file_path: Path):
    """
    Reads the pre-processed JSONL file and yields dictionaries.
    """
    data = []
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found.")
        return []
        
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def main():
    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
        tenant=TENANT,
        database=DATABASE,
    )

    # Clear existing data if you want a fresh start, otherwise get_or_create
    collection = client.get_or_create_collection(COLLECTION_NAME)

    # 1. Load data from the JSONL file instead of raw Markdown
    procedures = load_from_jsonl(JSONL_PATH)

    if not procedures:
        print("⚠️ No procedures found to ingest.")
        return

    # 2. Extract components for ChromaDB
    ids = [p["id"] for p in procedures]
    documents = [p["document"] for p in procedures]
    metadatas = [p["metadata"] for p in procedures]

    # 3. Add to Collection
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"✅ Ingested {len(ids)} procedures into `{COLLECTION_NAME}` from JSONL")

if __name__ == "__main__":
    main()