"""
search.py - Semantic vector search engine

At startup this module:
1. Loads the embedding model
2. Loads the local NumPy fallback embeddings and documents
3. Attempts to connect to Endee via the Python SDK

search() will first try the Endee SDK query.
If the Endee server is unavailable for any reason it transparently
falls back to the local NumPy cosine similarity search.
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer

# ─── Embedding Model ─────────────────────────────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── NumPy Fallback Resources ─────────────────────────────────────────────────
_base = os.path.dirname(__file__)

_docs_path = os.path.join(_base, "../data/docs_filtered.txt")
if not os.path.exists(_docs_path):
    _docs_path = os.path.join(_base, "../data/docs.txt")

with open(_docs_path, "r", encoding="utf-8") as _f:
    _documents = [line.strip() for line in _f.readlines() if line.strip()]

try:
    _embeddings = np.load(os.path.join(_base, "../data/embeddings.npy"))
except FileNotFoundError:
    _embeddings = None

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
    print("⚠️  'endee' package not installed — falling back to NumPy search.")
except Exception as exc:
    print(f"⚠️  Endee server not reachable ({exc}) — falling back to NumPy search.")


# ─── Search Function ──────────────────────────────────────────────────────────
def search(query: str, top_k: int = 3) -> list[str]:
    """
    Returns the top_k most semantically similar documents for the given query.

    Strategy:
      1. Try Endee SDK query() → extract meta["text"] from results
      2. On any failure, fall back to NumPy cosine similarity
    """
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    # ── Endee SDK path ────────────────────────────────────────────────────────
    if _endee_available and _endee_index is not None:
        try:
            results = _endee_index.query(vector=query_vector, top_k=top_k)
            texts = [
                r["meta"]["text"]
                for r in results
                if "meta" in r and "text" in r.get("meta", {})
            ]
            if texts:
                return texts
        except Exception as exc:
            print(f"⚠️  Endee query failed ({exc}), falling back to NumPy.")

    # ── NumPy Fallback path ───────────────────────────────────────────────────
    if _embeddings is None:
        return ["Knowledge base not indexed yet. Please run backend/ingest.py first."]

    similarities = np.dot(_embeddings, np.array(query_vector, dtype=np.float32))
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = [_documents[i] for i in top_indices if similarities[i] > 0.1]
    if not results:
        return ["No relevant context found. Try rephrasing your question."]
    return results
