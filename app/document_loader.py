import os
import json
import re
from typing import List
from langchain.docstore.document import Document

def load_documents_from_jsonl(folder_path: str, keywords: List[str] = []) -> List[Document]:
    documents = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        data = json.loads(line)
                        title = data.get("title", "").lower()
                        text = data.get("text", "").strip()

                        if text and (not keywords or any(kw in text.lower() for kw in keywords)):
                            documents.append(Document(
                                page_content=text,
                                metadata={"source": title}
                            ))
            except Exception as e:
                print(f"HATA ({file_path}): {e}")

    print(f"✅ Toplam {len(documents)} belge yüklendi.")
    return documents
