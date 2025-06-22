# 📜 Türkçe Tarih Chatbot

Bu proje, Türkçe Wikipedia’dan elde edilen içeriklere dayanarak tarih sorularına yanıt verebilen yapay zeka destekli bir chatbot geliştirmeyi amaçlamaktadır. Geliştirilen sistem, büyük dil modeli (LLM) olarak Google Gemini’yi kullanır ve belge arama işlemleri için FAISS vektör veritabanı ile entegre edilmiştir. Kullanıcı etkileşimi Streamlit tabanlı bir arayüz üzerinden gerçekleştirilir.

---

## 🎯 Proje Amacı

Amacımız, kullanıcıların Türkçe tarih sorularına Wikipedia verilerine dayalı, kaynak gösteren ve anlamlı yanıtlar almasını sağlamaktır. Bu sistem:

- Wikipedia içeriklerini işleyerek semantik bir belge veritabanı oluşturur.
- Kullanıcının sorduğu soruya benzer içerikleri bulur.
- Gemini LLM kullanarak doğal dilde ve kaynak referanslı bir yanıt üretir.

---

## 🧠 Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|----------|----------|
| **Streamlit** | Web tabanlı kullanıcı arayüzü |
| **LangChain** | Vektör tabanlı belge arama (FAISS) |
| **FAISS** | Belge embedding ve semantik arama |
| **Sentence-Transformers** | HuggingFace modeli ile embedding |
| **Google Generative AI (Gemini)** | Büyük dil modeliyle cevap üretimi |
| **dotenv** | Gizli anahtarların yönetimi (.env dosyası) |

---

## 🧩 Kurulum

### 1. Reponun Klonlanması

```bash
git clone https://github.com/ahmet-yasir/chatbot-tarih-qa.git
cd chatbot-tarih-qa
```

### 2. Gerekli Kütüphanelerin Kurulumu

```bash
pip install -r requirements.txt
```

### 3. `.env` Dosyasını Oluşturun

Proje dizinine `.env` adında bir dosya oluşturun ve içine aşağıdaki satırı ekleyin:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

> 🔑 **Not:** Google Gemini API anahtarınızı [Google AI Studio](https://makersuite.google.com/app) üzerinden ücretsiz olarak alabilirsiniz.

## 🗃️ Veri Seti Hazırlama

### 🔽 Wikipedia Dump İndirme

Wikipedia verisi [Wikimedia Dumps](https://dumps.wikimedia.org/trwiki/latest/) üzerinden indirilmektedir. Aşağıdaki komutları sırasıyla çalıştırarak veriyi `data/raw/` klasörüne indirebilirsiniz:

```bash
# data/raw klasörünü oluştur
mkdir -p data/raw

# Wikipedia verisini indir
wget -O data/raw/trwiki-latest-pages-articles.xml.bz2 \
https://dumps.wikimedia.org/trwiki/latest/trwiki-latest-pages-articles.xml.bz2
```
### 🛠️ WikiExtractor ile JSONL Formatına Dönüştürme

Wikipedia XML dump dosyasını işlemek için [WikiExtractor](https://github.com/attardi/wikiextractor) aracını kullanabilirsiniz. Aşağıdaki adımları takip edin:

#### WikiExtractor'ı klonlayın
```bash
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor
```

#### Gereksinimleri yükleyin
```bash
pip install -r requirements.txt
```
#### Wikipedia verisini işleyin ve çıktı olarak JSONL belgeleri üretin
```bash
python WikiExtractor.py \
  -o ../data/extracted \
  --json \
  --processes 4 \
  --bytes 100M \
  ../data/raw/trwiki-latest-pages-articles.xml.bz2
```
Bu işlem sonucunda data/extracted/ klasöründe .jsonl uzantılı birçok belge dosyası oluşacaktır.
Bu belgeler, embedding işlemiyle vektör veritabanına dönüştürülerek chatbot sisteminde kullanılacaktır.

## 🔨 Vektör Veritabanı Oluşturma

Veriler `.jsonl` formatında hazırlandıktan sonra, embedding (vektörleştirme) işlemi gerçekleştirilir. Bu işlem sonucunda FAISS formatında bir vektör veritabanı oluşturulur.

Aşağıdaki komutu kullanarak veritabanını oluşturabilirsiniz:

```bash
python build_vector_index.py
```
Bu komut şunları yapar:
- data/extracted/ klasöründen belgeleri yükler.
- sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 modeli ile her belgeyi  vektörleştirir.
- Vektörleri FAISS kullanarak vectorstore/faiss_index/ klasörüne kaydeder.

## 🖥️ Uygulamanın Başlatılması

Tüm kurulumlar tamamlandıktan ve vektör veritabanı oluşturulduktan sonra, Streamlit arayüzünü başlatmak için aşağıdaki komutu çalıştırın:

```bash
streamlit run app/streamlit_app.py
```
Komut çalıştırıldıktan sonra tarayıcınızda otomatik olarak bir arayüz açılır. Bu arayüz üzerinden Türkçe tarih sorularınızı sorabilirsiniz.
