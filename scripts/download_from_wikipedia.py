import wikipedia
import re
import os

# Türkçe Vikipedi kullan
wikipedia.set_lang("tr")

# GÜNCELLENMİŞ Konu başlıkları
KONULAR = [
    "TBMM'nin açılışı", "Kurtuluş Savaşı", "Sakarya Meydan Muharebesi", "Başkomutanlık Meydan Muharebesi",
    "Mudanya Ateşkes Antlaşması", "Lozan Antlaşması", "Cumhuriyetin ilanı", "Halifeliğin kaldırılması",
    "Şeyh Said İsyanı", "Takrir-i Sükûn Kanunu", "Menemen Olayı", "Atatürk", "Atatürk ilkeleri",
    "Atatürk devrimleri", "Kapitülasyonlar", "Köy Enstitüleri", "Nutuk (Mustafa Kemal Atatürk)", "İsmet İnönü",
    "II. Dünya Savaşı'nda Türkiye", "Demokrat Parti (1946)", "1946 Türkiye genel seçimleri",
    "1950 Türkiye genel seçimleri", "1954 Türkiye genel seçimleri", "1957 Türkiye genel seçimleri",
    "27 Mayıs Darbesi", "Adnan Menderes", "1961 Anayasası", "1965 Türkiye genel seçimleri",
    "12 Mart Muhtırası", "Bülent Ecevit", "1971 Türkiye'de askeri müdahale", "1974 Kıbrıs Harekâtı",
    "1977 Türkiye genel seçimleri", "Milliyetçi Cephe Hükümetleri", "1980 Darbesi", "1982 Anayasası",
    "Kenan Evren", "Turgut Özal", "Anavatan Partisi", "Necmettin Erbakan",
    "Refah Partisi", "28 Şubat Süreci", "Susurluk Skandalı", "PKK",
    "2001 Türkiye ekonomik krizi", "Adalet ve Kalkınma Partisi", "2002 Türkiye genel seçimleri",
    "2007 Cumhurbaşkanlığı krizi", "2010 Anayasa referandumu", "Gezi Parkı protestoları",
    "15 Temmuz darbe girişimi", "Cumhurbaşkanlığı Hükümet Sistemi",
    "2023 Türkiye genel seçimleri", "Recep Tayyip Erdoğan"
]

# Klasör oluştur
os.makedirs("data/raw", exist_ok=True)

# Sayfa çekme işlemi
for konu in KONULAR:
    try:
        sayfa = wikipedia.page(konu)
        metin = re.sub(r'\[\d+\]', '', sayfa.content)
        konu_dosya = konu.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "")
        dosya_adi = f"data/raw/{konu_dosya}.txt"
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(metin)
        print(f"✅ {konu} başarıyla kaydedildi.")
    except Exception as e:
        print(f"⚠️ {konu} indirilemedi: {e}")
