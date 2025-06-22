from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.document_loader import load_documents_from_jsonl
import os

def build_vectorstore(jsonl_folder: str, index_path: str, keywords: list = None) -> None:
    print("📄 Belgeler yükleniyor...")
    docs = load_documents_from_jsonl(jsonl_folder, keywords or [])

    print(f"✅ {len(docs)} belge yüklendi. Embedding başlatılıyor...")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)

    print("💾 FAISS indeks dosyası kaydediliyor...")
    vectorstore.save_local(index_path)
    print("✅ Tamamlandı.")

def load_vectorstore(index_path: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

