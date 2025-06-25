from app.retriever import build_vectorstore

if __name__ == "__main__":
    jsonl_folder = "data/extracted"
    index_path = "vectorstore/faiss_index"

    print("🔧 Vektör indeksi oluşturuluyor...")
    build_vectorstore(jsonl_folder, index_path, keywords=[])
    print(f"✅ FAISS indeksi başarıyla kaydedildi: {index_path}")
