## Ses Destekli AI Asistan
Bu proje, Gemini API'yi kullanarak sesli ve yazılı sohbet edebilen bir chatbot uygulamasıdır. Ayrıca, son 10 konuşmayı saklayan bir SQLite veritabanı kullanmaktadır.

## 🚀 Özellikler
* Gemini AI ile sohbet
* SQLite veritabanı ile son 10 konuşmayı kaydederek hafıza oluşturma
* Ses tanıma (SpeechRecognition)
* Sesli yanıt verme (pyttsx3)
* Yazılı veya sesli modda çalışma

## 🛠️ Kurulum
### 1️⃣ Gerekli Kütüphaneleri Kurun
```bash
pip install google-generativeai speechrecognition pyttsx3
```
### 2️⃣ API Anahtarınızı Ayarlayın
config.py dosyasındaki API_KEY değişkenine Gemini API anahtarınızı ekleyin:
```bash
API_KEY = "YOUR_GEMINI_API_KEY"
```
### 3️⃣ Veritabanını Oluşturulması
İlk çalıştırmada main.py dosyası, veritabanını otomatik olarak oluşturacaktır.

## 📌 Kullanım
Programı çalıştırın ardından yazarak iletişim kurmak isterseniz y , konuşarak iletişim kurmak isterseniz ise s yazarak devam edin.

## 🔚 Çıkış
Chatbot'tan çıkmak için "çıkış" yazın veya söyleyin.

## 📂 Dosya Açıklamaları
* main.py → Ana chatbot dosyası.
* database.py → SQLite veritabanı işlemleri.
* config.py → API anahtarını saklayan yapılandırma dosyası.
