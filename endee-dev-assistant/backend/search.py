"""
search.py - Semantic vector search engine

At startup this module:
1. Loads the embedding model
2. Attempts to connect to Endee via the Python SDK

search() will exclusively try the Endee SDK query.
If the Endee server is unavailable, it will return an explicit error message.
"""

import os
from sentence_transformers import SentenceTransformer

# ─── Embedding Model ─────────────────────────────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── Endee SDK Connection ─────────────────────────────────────────────────────
_endee_index = None
_endee_available = False

try:
    import endee as _endee_module

    _client = _endee_module.Endee(token="local:local")
    _client.set_base_url("http://localhost:8080")

    INDEX_NAME = "devassist"
    _endee_index = _client.get_index(INDEX_NAME)
    _endee_available = True
    print(f"✅ Endee SDK connected — using index '{INDEX_NAME}'")

except ImportError:
    print("⚠️  'endee' package not installed.")
except Exception as exc:
    print(f"⚠️  Endee server not reachable ({exc}).")


# ─── Search Function ──────────────────────────────────────────────────────────
def search(query: str, top_k: int = 3) -> list[str]:
    """
    Returns the top_k most semantically similar documents for the given query.

    Strategy:
      1. Try Endee SDK query() → extract meta["text"] from results
      2. On failure, return a loud error instructing the user to start Endee.
    """
    if not _endee_available or _endee_index is None:
         return ["Error: Endee Vector Database is not reachable. Please ensure the server is running on port 8080."]

    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    # ── Endee SDK path ────────────────────────────────────────────────────────
    try:
        results = _endee_index.query(vector=query_vector, top_k=top_k)
        texts = [
            r["meta"]["text"]
            for r in results
            if "meta" in r and "text" in r.get("meta", {})
        ]
        if texts:
            return texts
        else:
            return ["No relevant context found in the knowledge base. Try asking about Python, FastAPI, React, Docker, Git, or machine learning."]
    except Exception as exc:
        print(f"⚠️  Endee query failed ({exc}).")
        return [f"Error querying Endee Vector Database: {exc}. Ensure the server is healthy."]

