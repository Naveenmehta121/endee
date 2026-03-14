from sentence_transformers import SentenceTransformer
import numpy as np
import requests
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

# We will load the exact documents we encoded
docs_path = "../data/docs_filtered.txt"
if not os.path.exists(docs_path):
    docs_path = "../data/docs.txt"

with open(docs_path, "r", encoding="utf-8") as f:
    documents = [doc.strip() for doc in f.readlines() if doc.strip()]

try:
    embeddings = np.load("../data/embeddings.npy")
except FileNotFoundError:
    embeddings = None

def search(query, top_k=2, threshold=0.3):
    query_vector = model.encode(query).tolist()
    
    payload = {
        "vector": query_vector,
        "top_k": top_k
    }

    try:
        response = requests.post(
            "http://localhost:8080/api/v1/vectors/search",
            json=payload,
            timeout=1
        )
        response.raise_for_status()
        return response.json()

    except:
        print("Endee server not running - using fallback search")
        if embeddings is None:
            return ["Fallback numpy embeddings not found."]
            
        # Fallback to local Numpy vector search
        query_embedding = model.encode([query], normalize_embeddings=True)[0]
        similarities = np.dot(embeddings, query_embedding)
        
        results = []
        top_indices = np.argsort(similarities)[::-1]
        
        for i in top_indices:
            if similarities[i] >= threshold and len(results) < top_k:
                results.append(documents[i])
                
        return results
