import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect("fiyatlandirma_tahmin.db")
cursor = conn.cursor()


try:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT baslik, konu, anahtar_kelime, kullanici_adi, tarih_saat
        FROM web_scraping_verileri
        WHERE kullanici_id = ?
        ORDER BY tarih_saat DESC  -- Verileri yeniden eskiye sıralar""")
    rows = cursor.fetchall()

    
except sqlite3.Error as e:
    print(f"Veritabanı hatası: {e}")