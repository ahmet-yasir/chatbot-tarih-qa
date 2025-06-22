import os
import json
import re
from typing import List
from langchain.docstore.document import Document

def clean_paragraph(text: str) -> str:
    """
    Paragrafı temizler:
    - Kaynakça veya başlık gibi bölümleri atar
    - Boşlukları düzeltir
    - [1], [2] gibi referansları siler
    - Kısa/önemsiz paragrafları filtreler
    """
    # == Kaynakça == gibi başlıkları atla
    if re.search(r"^={2,}.*={2,}$", text):
        return ""
    
    # Boşlukları düzelt
    text = re.sub(r"\s+", " ", text).strip()
    
    # Dipnot referanslarını kaldır [1], [2] vb.
    text = re.sub(r"\[\d+\]", "", text)

    # Anlamlı uzunlukta değilse at
    if len(text.split()) < 10:
        return ""
    
    return text

def load_documents_from_jsonl(folder_path: str, keywords: List[str] = []) -> List[Document]:
    """
    Belirtilen klasördeki .jsonl dosyalarını okuyarak filtrelenmiş Document nesneleri üretir.
    """
    documents = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        data = json.loads(line)
                        title = data.get("title", "").lower()
                        text = data.get("text", "")

                        for paragraph in text.split("\n"):
                            paragraph = clean_paragraph(paragraph)
                            if paragraph and (not keywords or any(kw in paragraph.lower() for kw in keywords)):

                                documents.append(Document(
                                    page_content=paragraph,
                                    metadata={"source": title}
                                ))
            except Exception as e:
                print(f"HATA ({file_path}): {e}")

    print(f"✅ Toplam {len(documents)} filtrelenmiş belge yüklendi.")
    return documents
