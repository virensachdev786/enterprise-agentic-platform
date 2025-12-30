import json
import os
import chromadb

# Connect to Chroma HTTP server
client = chromadb.HttpClient(
    host="localhost",
    port=8050
)

COLLECTION_NAME = "policy_kb"

# Create or get collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"description": "Password Reset Security Policies"}
)

print(f"Using Collection: {COLLECTION_NAME}")

docs = []
ids = []
metas = []

# Get the path to chunks.jsonl relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
chunks_path = os.path.join(script_dir, "..", "chunks.jsonl")

with open(chunks_path, "r") as file:
    for line in file:
        chunk = json.loads(line)

        ids.append(chunk["id"])
        docs.append(chunk["text"])
        metas.append(chunk["metadata"])

# Insert into Chroma
collection.upsert(
    ids=ids,
    documents=docs,
    metadatas=metas
)

print(f"Ingested {len(ids)} policy chunks successfully!")

