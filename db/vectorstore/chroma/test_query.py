import chromadb

client = chromadb.HttpClient(host="localhost", port=8050)
collection = client.get_collection("policy_kb")

results = collection.query(
    query_texts=["What is policy for remote reset?"],
    n_results=3
)

print(results)

