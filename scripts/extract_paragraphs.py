import os

input_dir = "data/raw"
output_file = "data/processed/rag_paragraflar.txt"
os.makedirs("data/processed", exist_ok=True)

with open(output_file, "w", encoding="utf-8") as out_f:
    for fname in os.listdir(input_dir):
        with open(os.path.join(input_dir, fname), "r", encoding="utf-8") as in_f:
            text = in_f.read()
            paragraflar = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
            for p in paragraflar:
                out_f.write(p + "\n\n")
                
print(f"Paragraflar {output_file} dosyasına kaydedildi.")