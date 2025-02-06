import google.generativeai as genai
from database import create_table, save_message, get_last_10_messages

# API Anahtarını Ayarla
genai.configure(api_key="GEMINI_API_KEY")

# Modeli Başlat
model = genai.GenerativeModel("gemini-pro")

# Veritabanını oluştur
create_table()

def chat_gemini(prompt):
    # Son 10 konuşmayı al
    history = "\n".join(get_last_10_messages())

    # Sohbeti Gemini'ye gönder
    full_prompt = f"{history}\nSen: {prompt}"
    response = model.generate_content(full_prompt)

    # Yanıtı al ve kaydet
    save_message(prompt, response.text)

    return response.text

while True:
    user_input = input("Sen: ")
    if user_input.lower() == "çıkış":
        break
    response = chat_gemini(user_input)
    print("Chatbot:", response)
