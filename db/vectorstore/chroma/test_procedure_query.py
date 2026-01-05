import chromadb
from pathlib import Path

# Chroma Config
CHROMA_HOST = "localhost"
CHROMA_PORT = 8050
TENANT = "default_tenant"
DATABASE = "default_database"
COLLECTION_NAME = "procedures_kb"

def query_procedure(intent: str, system: str):
    """
    Queries ChromaDB for a specific procedure based on intent and system.
    """
    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
        tenant=TENANT,
        database=DATABASE,
    )

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection = client.get_collection(COLLECTION_NAME)
    all_metadatas = collection.get(include=['metadatas'])['metadatas']
    print(f"Current Metadata in DB: {all_metadatas}")

    print(f"🔍 Searching for: Intent='{intent}', System='{system}'...")

    # Querying with Metadata filtering
    # This ensures we get the EXACT procedure for the detected intent
    results = collection.query(
        query_texts=[f"How to handle {intent} for {system}"],
        n_results=1,
        where={
            "$and": [
                {"intent": intent},
                {"system": system}
            ]
        }
    )

    if results['documents'] and len(results['documents'][0]) > 0:
        doc = results['documents'][0][0]
        meta = results['metadatas'][0][0]
        print("\n✅ Found Procedure Match:")
        print(f"--- [ID: {results['ids'][0][0]}] ---")
        print(f"Procedure Content:\n{doc}")
        return doc
    else:
        print("\n❌ No matching procedure found for this intent/system combination.")
        return None

if __name__ == "__main__":
    
    print("\n" + "="*50 + "\n")

    # Test Case 1: Standard Password Reset
    query_procedure(intent="password_reset", system="ServiceNow")
    
    print("\n" + "="*50 + "\n")
    
    # Test Case 2: Unknown
    query_procedure(intent="unknown", system="ServiceNow")

    print("\n" + "="*50 + "\n")
    
    # Test Case 3: Knowledge Question
    query_procedure(intent="knowledge_question", system="unknown")

