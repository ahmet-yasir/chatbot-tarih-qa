import google.generativeai as genai
import os

def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")  # .env dosyasından al
    genai.configure(api_key=api_key)

    generation_config = genai.types.GenerationConfig(
        temperature=0.4,  # 🔥 Burayı değiştirerek yaratıcı ya da tutarlı yanıtlar alabilirsin
        max_output_tokens=512,
        top_p=0.8,
        top_k=10
    )

    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        generation_config=generation_config
    )
    return model
