import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.retriever import load_vectorstore
from app.llm_setup import get_llm
from dotenv import load_dotenv

load_dotenv()

# === FAISS indeks yolunu tanımla ===
VECTORSTORE_PATH = "vectorstore/faiss_index"

# === Başlat ===
st.set_page_config(page_title="Tarih Chatbot", layout="wide")
st.title("📜 Türkçe Tarih Chatbot")
st.markdown("Tarihle ilgili sorularınızı sorun. Wikipedia tabanlı LLM yanıtlasın.")

# === Soru al ===
question = st.text_input("❓ Soru:", placeholder="Örn: Tanzimat Fermanı ne zaman ilan edildi?")

if question:
    with st.spinner("🔍 Yanıt aranıyor..."):
        # 1. Vektör veritabanını yükle
        vectorstore = load_vectorstore(VECTORSTORE_PATH)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(question)

        # 2. Gemini için prompt oluştur
        context = "\n\n".join([doc.page_content for doc in docs])
        # Her belgeyi ayrı olarak kaynak göstererek yapılandıralım
        sources = []
        for i, doc in enumerate(docs):
            sources.append(f"[{i+1}] {doc.page_content.strip()}")
        source_text = "\n\n".join(sources)

        prompt = f"""Aşağıda numaralanmış bazı kaynak metinler verilmiştir. Bu kaynaklara dayanarak kullanıcı sorusunu Türkçe olarak, mümkünse kaynak numarası vererek yanıtla. Cevabın başında kısa bir özet, ardından detaylı açıklama olsun.

        Kaynaklar:
        {source_text}

        Soru: {question}
        Yanıt (kaynak numarasıyla belirt):"""


        # 3. Gemini LLM ile yanıt üret
        llm = get_llm()
        response = llm.generate_content(prompt)
        answer = response.text

        # 4. Sonuçları göster
        st.success("📘 Cevap:")
        st.markdown(answer)  # st.write yerine markdown, link/numara içeriği destekler

        # 5. Kullanılan belgeleri göster
        with st.expander("🔎 Kullanılan belgeler"):
            for i, doc in enumerate(docs):
                st.markdown(f"**[{i+1}] Kaynak:** {doc.metadata['source'].title()}")
                st.write(doc.page_content[:300] + "...")

    # === Geçmiş soruları sakla === 
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.session_state["history"].append((question, answer))

    st.markdown("### 🕓 Geçmiş Sorular")
    for q, a in reversed(st.session_state["history"][-5:]):
        st.markdown(f"**Soru:** {q}")
        st.markdown(f"**Yanıt:** {a}")



