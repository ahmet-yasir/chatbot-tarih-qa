# 🔨 Vektör veritabanı oluşturma scripti

from app.retriever import build_vectorstore

if __name__ == "__main__":
    jsonl_folder = "data/extracted"              # WikiExtractor çıktıları
    index_path = "vectorstore/faiss_index"       # FAISS indeksin kaydedileceği yer

    build_vectorstore(jsonl_folder, index_path, keywords=[])
