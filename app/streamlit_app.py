import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
from app.retriever import load_vectorstore
from app.llm_setup import get_llm

# Ortam değişkenlerini yükle (.env içindeki GEMINI_API_KEY)
load_dotenv()

# FAISS indeks dizini
VECTORSTORE_PATH = "vectorstore/faiss_index"

# Streamlit ayarları
st.set_page_config(page_title="🇹🇷 Cumhuriyet Tarihi Chatbot", layout="wide")
st.title("📜 Cumhuriyet Tarihi Chatbot")
st.markdown("Cumhuriyet tarihiyle ilgili sorularınızı aşağıya yazın. Sistem, Wikipedia kaynaklarını kullanarak cevap üretecektir.")

# Kullanıcıdan soru al
question = st.text_input("❓ Sorunuz:", placeholder="Örn: 1980 darbesi ne zaman gerçekleşti?")

if question:
    with st.spinner("🔍 Yanıt hazırlanıyor..."):
        # 1. Vektör veritabanını yükle
        vectorstore = load_vectorstore(VECTORSTORE_PATH)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.get_relevant_documents(question)

        # 2. Kaynakları hazırlama
        sources = [f"[{i+1}] {doc.page_content.strip()}" for i, doc in enumerate(docs)]
        source_text = "\n\n".join(sources)

        # 3. Sistem prompt (Gemini için detaylı)
        prompt = f"""
Sen bir Cumhuriyet tarihi uzmanı gibi davranan Türkçe dilinde konuşan bir yapay zekasın.

Aşağıda Türkiye Cumhuriyeti tarihine ait Wikipedia kaynaklarından alınmış numaralandırılmış paragraflar bulunmaktadır. 
Görevin, yalnızca bu kaynaklara dayanarak kullanıcının sorduğu soruya **Türkçe** olarak cevap vermektir.

### KURALLAR:
- Cevabın **başında kısa ve öz bir özet**, ardından **ayrıntılı açıklama** olsun.
- Yalnızca **verilen kaynak paragraflarına dayanarak** yanıt ver. Tahmin yürütme, dış bilgi ekleme.
- **Kaynak numaralarını mutlaka belirt.** Örneğin: “(bkz: [1])” gibi.
- Eğer sorunun cevabı kaynaklar içinde yer almıyorsa bunu açıkça belirt: “Verilen kaynaklarda bu soruya doğrudan bir yanıt bulunmamaktadır.”
- Gerektiğinde paragrafları birleştirerek kapsamlı ama tutarlı bir yanıt oluştur.

### KAYNAKLAR:
{source_text}

### SORU:
{question}

### YANIT (lütfen kaynak numarasıyla birlikte yanıtla):
"""

        # 4. Gemini modelinden yanıt al
        llm = get_llm()
        response = llm.generate_content(prompt)
        answer = response.text

        # 5. Yanıtı göster
        st.success("📘 Cevap:")
        st.markdown(answer)

        # 6. Kaynakları ayrı alanda göster
        with st.expander("🔎 Kullanılan kaynaklar"):
            for i, doc in enumerate(docs):
                st.markdown(f"**[{i+1}] Kaynak:** {doc.metadata['source'].title()}")
                st.write(doc.page_content[:300] + "...")

        # 7. Geçmişi güncelle
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append((question, answer))

# 8. Geçmiş soruları göster
if "history" in st.session_state and st.session_state["history"]:
    st.markdown("### 🕓 Geçmiş Sorular")
    for q, a in reversed(st.session_state["history"][-5:]):
        st.markdown(f"**Soru:** {q}")
        st.markdown(f"**Yanıt:** {a}")
