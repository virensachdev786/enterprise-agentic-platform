import chromadb  # pyright: ignore[reportMissingImports]

client = chromadb.HttpClient(host="localhost", port=8050)
collection = client.get_collection("policy_kb")

results = collection.query(
    query_texts=["Hello Id Like your help with resetting my password"],
    n_results=3
)

print(results)

