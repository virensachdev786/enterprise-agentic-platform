import chromadb
import os
from typing import List, Dict


class KnowledgeRetriever:
    """
    Thin wrapper over Chroma.
    No scoring logic. No business rules.
    """

    def __init__(
        self,
        collection_name: str,
        host: str = "localhost",
        port: int = 8050,
        tenant: str = "default_tenant",
        database: str = "default_database",
    ):
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            tenant=tenant,
            database=database,
        )
        self.collection = self.client.get_collection(collection_name)

    def query(self, text: str, top_k: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[text],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]  # Added distances
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]  # Added distances

        print(f"\n--- RETRIEVAL DEBUG: {text} ---")
        formatted_results = []
        for doc, meta, dist in zip(docs, metas, distances):
            # Distance 0.0 means identical. High distance (e.g., > 1.4) means unrelated.
            print(f"-> Score: {dist:.4f} | Type: {meta.get('type')} | Snippet: {doc[:50]}...")
            
            formatted_results.append({
                "content": doc,
                "metadata": meta,
                "score": dist  # Pass score to the planner
            })
        print("-------------------------------\n")

        return formatted_results
