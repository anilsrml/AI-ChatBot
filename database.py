import sqlite3


def connect_db():
    return sqlite3.connect("chat_history.db")


def create_tables():
    """Son 10 konuşmayı saklamak için tablo oluşturur."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(user_message, bot_response):
    """Yeni konuşmayı veritabanına kaydeder ve 10'dan fazla olursa en eskiyi siler."""
    conn = connect_db()
    cursor = conn.cursor()

    # Yeni konuşmayı ekle
    cursor.execute("INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
                   (user_message, bot_response))
    conn.commit()

    # Eğer 10'dan fazla konuşma varsa, en eskisini sil
    cursor.execute("SELECT COUNT(*) FROM conversations")
    count = cursor.fetchone()[0]

    if count > 10:
        cursor.execute("DELETE FROM conversations WHERE id = (SELECT id FROM conversations ORDER BY id ASC LIMIT 1)")
        conn.commit()

    conn.close()


def get_last_conversations(limit=10):
    """Son N konuşmayı getirir. (Varsayılan: 10 adet)"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_message, bot_response 
        FROM conversations 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))
    results = cursor.fetchall()
    conn.close()

    # Konuşmaları formatla ve eski sırayla döndür
    conversations = []
    for user_msg, bot_resp in reversed(results):
        conversations.append(f"Kullanıcı: {user_msg}\nBot: {bot_resp}")

    return conversations