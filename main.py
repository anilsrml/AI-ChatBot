import google.generativeai as genai
from database import create_tables, save_conversation, get_last_conversations
from config import API_KEY
import speech_recognition as sr
import pyttsx3

# Gemini API'yi başlat
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Sesli yanıt motoru başlat
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Konuşma hızını ayarla

# Veritabanını oluştur
create_tables()


def chat_gemini(prompt):
    """Chatbot ile konuşmayı yönetir ve hafızayı son konuşmalardan sağlar."""
    conversations = get_last_conversations()  # Son konuşmaları al

    # Chatbot'a verilecek metni oluştur
    context = "\n".join(conversations) if conversations else ""
    full_prompt = f"Önceki konuşmalar:\n{context}\n\nKullanıcı: {prompt}"

    try:
        response = model.generate_content(full_prompt)

        if response and response.text:
            # Yanıttan "Chatbot:" veya "Ben:" gibi önekleri temizle
            clean_response = response.text
            prefixes_to_remove = ["Chatbot:", "Ben:", "Bot:"]
            for prefix in prefixes_to_remove:
                if clean_response.startswith(prefix):
                    clean_response = clean_response[len(prefix):].strip()

            # Konuşmayı kaydet
            save_conversation(prompt, clean_response)
            return clean_response
        else:
            print("Chatbot yanıtı alınamadı.")
            return "Üzgünüm, şu anda yanıt veremiyorum."
    except Exception as e:
        print(f"Chatbot yanıtı alınırken hata oluştu: {e}")
        return "Bir hata oluştu, lütfen tekrar deneyin."


def speak(text):
    """Chatbot'un metni sesli okumasını sağlar."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Sesli yanıt vermede hata oluştu: {e}")


def listen():
    """Kullanıcının sesli komutunu dinler ve metne çevirir."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Dinliyorum... (Mikrofon açılıyor)")
        try:
            audio = recognizer.listen(source, timeout=10)  # Bekleme süresini artır
            text = recognizer.recognize_google(audio, language="tr-TR")  # Türkçe dil desteği
            print(f"Sen: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Söylediğinizi anlayamadım, lütfen tekrar edin.")
            return None
        except sr.RequestError:
            print("Ses tanıma servisine ulaşılamıyor. İnternet bağlantınızı kontrol edin.")
            return None


# Ana döngüde çıktı formatını düzelt
if __name__ == "__main__":
    print("Chatbot'a hoş geldiniz! (Çıkış için 'çıkış' yazın veya 'çıkış' deyin.)")

    while True:
        mode = input("Sesli konuşmak için 's', yazılı sohbet için 'y' girin: ").lower()

        if mode == "s":
            while True:
                user_input = listen()
                if user_input is None:
                    continue
                if "çıkış" in user_input:
                    print("Chatbot kapanıyor...")
                    speak("Chatbot kapanıyor, görüşmek üzere.")
                    break
                response = chat_gemini(user_input)
                print(f"Bot: {response}")  # Çıktı formatını düzelt
                speak(response)

        elif mode == "y":
            while True:
                user_input = input("Sen: ")
                if user_input.lower() == "çıkış":
                    print("Chatbot kapanıyor...")
                    break
                response = chat_gemini(user_input)
                print(f"ChatBot: {response}")  # Çıktı formatını düzelt