import os
import markdown
from bs4 import BeautifulSoup

def markdown_to_text(md_content: str) -> str:
    """
    Convert Markdown content to clean plain text.
    """
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def chunk_text(text: str, max_words: int = 250):
    """
    Split text into chunks of approximately `max_words` words.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks

def process_markdown_folder(folder_path: str):
    """
    Read all .md files in `folder_path`, convert to text,
    split into chunks, and return [(chunk_text, metadata), ...].
    """
    all_chunks = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)

                with open(full_path, "r", encoding="utf-8") as f:
                    md_content = f.read()

                plain_text = markdown_to_text(md_content)
                chunks = chunk_text(plain_text)

                for idx, chunk in enumerate(chunks):
                    metadata = {
                        "file": file,
                        "chunk_id": idx
                    }
                    all_chunks.append((chunk, metadata))

    return all_chunks

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCS_DIR = os.path.join(BASE_DIR, "..", "docs")

    chunks = process_markdown_folder(DOCS_DIR)

    print(f"Total chunks created: {len(chunks)}")

    if chunks:
        print("\n--- Sample Chunk ---")
        print(chunks[0][0])
        print("Metadata:", chunks[0][1])