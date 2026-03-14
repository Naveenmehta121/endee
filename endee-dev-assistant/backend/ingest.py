"""
ingest.py - Embedding generation and vector database ingestion

This script:
1. Loads the knowledge base documents from docs.txt
2. Generates sentence embeddings using all-MiniLM-L6-v2
3. Saves a local NumPy fallback (always works offline)
4. Attempts to upsert all vectors into the Endee vector database
   using the official Python SDK
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer

# ─── Load Embedding Model ────────────────────────────────────────────────────
print("[1/4] Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── Load Documents ──────────────────────────────────────────────────────────
docs_path = os.path.join(os.path.dirname(__file__), "../data/docs.txt")
with open(docs_path, "r", encoding="utf-8") as f:
    documents = [line.strip() for line in f.readlines() if line.strip()]

print(f"[2/4] Loaded {len(documents)} documents from knowledge base.")

# ─── Generate Embeddings ─────────────────────────────────────────────────────
print("[3/4] Generating embeddings...")
embeddings = model.encode(documents, normalize_embeddings=True)

# Always save NumPy fallback first so local search always works
np.save(os.path.join(os.path.dirname(__file__), "../data/embeddings.npy"), embeddings)

# Save filtered docs to guarantee index alignment with embeddings
filtered_path = os.path.join(os.path.dirname(__file__), "../data/docs_filtered.txt")
with open(filtered_path, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc + "\n")

print(f"✅ Embeddings saved locally. ({len(documents)} vectors, dim=384)")

# ─── Endee SDK Upsert ────────────────────────────────────────────────────────
print("[4/4] Attempting to connect to Endee vector database...")

try:
    import endee

    # Initialize the Endee client pointing at the local Docker instance
    client = endee.Endee(token="local:local")
    client.set_base_url("http://localhost:8080")

    INDEX_NAME = "devassist"
    DIMENSION  = 384        # all-MiniLM-L6-v2 output dimension
    SPACE_TYPE = "cosine"   # use cosine similarity

    # Create index (idempotent - catches AlreadyExists errors gracefully)
    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            space_type=SPACE_TYPE,
        )
        print(f"   Created Endee index '{INDEX_NAME}'.")
    except Exception as exc:
        print(f"   Index '{INDEX_NAME}' already exists or creation skipped: {exc}")

    # Get index handle
    idx = client.get_index(INDEX_NAME)

    # Build the upsert payload: list of dicts with id, vector, meta
    batch = [
        {
            "id":     f"doc_{i}",
            "vector": embeddings[i].tolist(),
            "meta":   {"text": doc},
        }
        for i, doc in enumerate(documents)
    ]

    # Upsert all vectors in a single batch call
    idx.upsert(batch)
    print(f"✅ Successfully upserted {len(batch)} vectors into Endee index '{INDEX_NAME}'!")

except ImportError:
    print("⚠️  'endee' package not installed. Run: pip install endee")
except Exception as exc:
    print(f"⚠️  Endee server unavailable ({exc}). Local NumPy fallback will be used instead.")

print("\nIngestion complete.")
