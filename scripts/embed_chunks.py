import os
import pickle
from sentence_transformers import SentenceTransformer
from chunk_md import process_markdown_folder

# Resolve paths safely (important!)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "..", "docs")
INDEX_DIR = os.path.join(BASE_DIR, "..", "index")

os.makedirs(INDEX_DIR, exist_ok=True)

def generate_embeddings():
    # Load SBERT model (downloads in Codespaces)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load chunks
    chunks_with_meta = process_markdown_folder(DOCS_DIR)

    if not chunks_with_meta:
        raise RuntimeError("No chunks found. Check docs directory.")

    texts = [chunk for chunk, _ in chunks_with_meta]
    metadata = [meta for _, meta in chunks_with_meta]

    print(f"Generating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(texts, show_progress_bar=True)

    return embeddings, metadata, texts

if __name__ == "__main__":
    embeddings, metadata, texts = generate_embeddings()

    print("Embedding shape:", embeddings.shape)
    print("Sample vector length:", len(embeddings[0]))

    output_path = os.path.join(INDEX_DIR, "embeddings.pkl")

    with open(output_path, "wb") as f:
        pickle.dump(
            {
                "embeddings": embeddings,
                "metadata": metadata,
                "texts": texts,
            },
            f
        )

    print(f"✅ Embeddings saved to {output_path}")