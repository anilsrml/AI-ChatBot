import sqlite3

# Veritabanı bağlantısını oluştur
def connect_db():
    return sqlite3.connect("chat_history.db")


# Veritabanını ve tabloyu oluştur
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()


# Konuşmayı kaydet
def save_message(user_message, bot_response):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()


# Son 10 konuşmayı getir
def get_last_10_messages():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chat ORDER BY id DESC LIMIT 10")
    messages = cursor.fetchall()
    conn.close()

    return [f"Sen: {msg[0]}\nChatbot: {msg[1]}" for msg in messages[::-1]]  # Eski mesajları sırayla döndür
