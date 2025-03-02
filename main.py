import google.generativeai as genai
from database import create_tables, save_conversation, get_last_conversations
from config import API_KEY
import speech_recognition as sr
import pyttsx3

# 🌟 API'yi başlat
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# 🎙️ Sesli yanıt motorunu başlat
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Konuşma hızını ayarla

# 📂 Veritabanını oluştur
create_tables()

def chat_gemini(prompt):
    """Chatbot ile konuşmayı yönetir ve son konuşmalardan bağlam sağlar."""
    conversations = get_last_conversations()
    context = "\n".join(conversations) if conversations else ""
    full_prompt = f"Önceki konuşmalar:\n{context}\n\nKullanıcı: {prompt}"

    try:
        response = model.generate_content(full_prompt)

        if response and response.text:
            clean_response = response.text.strip()
            for prefix in ["Chatbot:", "Ben:", "Bot:"]:
                if clean_response.startswith(prefix):
                    clean_response = clean_response[len(prefix):].strip()

            save_conversation(prompt, clean_response)
            return clean_response
        return "Üzgünüm, şu anda yanıt veremiyorum."

    except Exception as e:  # Daha genel hata yakalama
        print(f"⚠️ Chatbot hata verdi: {e}")
        return "Bir hata oluştu, lütfen tekrar deneyin."


def speak(text):
    """Metni sesli okur."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Sesli yanıt hatası: {e}")


def listen():
    """Kullanıcının sesli girişini alır ve metne çevirir."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Dinliyorum...")
        try:
            audio = recognizer.listen(source, timeout=20)
            text = recognizer.recognize_google(audio, language="tr-TR") 
            return text.lower()
        except sr.UnknownValueError:
            return None  # Kullanıcı net konuşmazsa None döndür
        except sr.RequestError:
            return "Bağlantı hatası"


def chat_loop(mode):
    """Yazılı veya sesli chat modunu çalıştırır."""
    while True:
        if mode == "s":
            user_input = listen()
            if user_input is None:
                continue
        else:
            user_input = input("Sen: ").strip().lower()

        if user_input == "çıkış":
            print("🔴 Chatbot kapanıyor...")
            speak("Chatbot kapanıyor, görüşmek üzere.")
            break

        response = chat_gemini(user_input)
        print(f"Bot: {response}")
        speak(response)


if __name__ == "__main__":
    print("🤖 Chatbot'a hoş geldiniz! ('çıkış' yazarak çıkabilirsiniz.)")
    mode = input("🎙️ Sesli mod için 's', yazılı sohbet için 'y' girin: ").strip().lower()

    if mode in ["s", "y"]:
        chat_loop(mode)
    else:
        print("Geçersiz giriş! Program kapanıyor.")
