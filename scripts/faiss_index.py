import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Resolve paths safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(BASE_DIR, "..", "index")
EMBEDDINGS_PATH = os.path.join(INDEX_DIR, "embeddings.pkl")
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")

def load_embeddings():
    with open(EMBEDDINGS_PATH, "rb") as f:
        data = pickle.load(f)
    return data["embeddings"], data["texts"], data["metadata"]

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]

    # Simple, exact index (good for learning)
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings.astype("float32"))
    return index

def save_faiss_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)

def semantic_search(query, model, index, texts, top_k=3):
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append(texts[idx])

    return results

if __name__ == "__main__":
    print("Loading persisted embeddings...")
    embeddings, texts, metadata = load_embeddings()

    print(f"Loaded {len(texts)} embeddings")

    print("Building FAISS index...")
    index = build_faiss_index(embeddings)

    save_faiss_index(index)
    print("✅ FAISS index saved")

    print("\nRunning test semantic search...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    results = semantic_search(
        query="How is documentation deployed?",
        model=model,
        index=index,
        texts=texts,
        top_k=3
    )

    print("\nTop semantic results:")
    for r in results:
        print("-", r)