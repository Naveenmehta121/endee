from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents
with open("../data/docs.txt", "r", encoding="utf-8") as f:
    documents = f.readlines()

# Filter out empty lines to avoid empty embeddings
documents = [doc.strip() for doc in documents if doc.strip()]

# Generate embeddings (normalized for cosine similarity)
print("Generating embeddings...")
embeddings = model.encode(documents, normalize_embeddings=True)

# Save embeddings
np.save("../data/embeddings.npy", embeddings)

# We should also save the filtered documents so search.py uses the exact same indices
with open("../data/docs_filtered.txt", "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc + "\n")

print("Embeddings generated and saved successfully!")
