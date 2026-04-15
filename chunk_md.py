import os
import markdown
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def markdown_to_text(md_content):
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ")

def chunk_text(text, max_words=250):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks

def process_markdown_folder(folder_path):
    all_chunks = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                text = markdown_to_text(content)
                chunks = chunk_text(text)

                for idx, chunk in enumerate(chunks):
                    meta = {
                        "file": file,
                        "chunk_id": idx
                    }
                    all_chunks.append((chunk, meta))

    return all_chunks

if __name__ == "__main__":
    docs_path = os.path.join(BASE_DIR, "..", "docs")
    chunks = process_markdown_folder(docs_path)

    print(f"Total chunks created: {len(chunks)}")

    if chunks:
        print("\n--- Sample Chunk ---")
        print(chunks[0][0])
        print("Metadata:", chunks[0][1])