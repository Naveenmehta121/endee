from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# We will load the exact documents we encoded
docs_path = "../data/docs_filtered.txt"
import os
if not os.path.exists(docs_path):
    docs_path = "../data/docs.txt"

with open(docs_path, "r", encoding="utf-8") as f:
    documents = [doc.strip() for doc in f.readlines() if doc.strip()]

embeddings = np.load("../data/embeddings.npy")

def search(query, top_k=2, threshold=0.3):
    # Encode with normalization for cosine similarity
    query_embedding = model.encode([query], normalize_embeddings=True)[0]

    # Compute cosine similarity
    similarities = np.dot(embeddings, query_embedding)

    # Filter by threshold and get top indices
    results = []
    top_indices = np.argsort(similarities)[::-1]
    
    for i in top_indices:
        if similarities[i] >= threshold and len(results) < top_k:
            results.append(documents[i])
            
    return results
