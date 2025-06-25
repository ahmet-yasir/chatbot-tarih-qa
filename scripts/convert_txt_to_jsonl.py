import os
import json

input_file = "data/processed/rag_paragraflar.txt"
output_folder = "data/extracted"
os.makedirs(output_folder, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f:
    paragraphs = [p.strip() for p in f.read().split("\n\n") if len(p.strip()) > 0]

output_file = os.path.join(output_folder, "cumhuriyet_paragraflar.jsonl")

with open(output_file, "w", encoding="utf-8") as out_f:
    for i, p in enumerate(paragraphs):
        obj = {"title": f"paragraf_{i}", "text": p}
        out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"✅ {len(paragraphs)} paragraf JSONL formatında kaydedildi: {output_file}")
