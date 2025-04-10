import sqlite3
import pandas as pd
import numpy as np
# Veritabanına bağlan
conn = sqlite3.connect("fiyatlandirma_tahmin.db")
cursor = conn.cursor()

# `kullanicilar` tablosunu oluştur
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS kullanicilar (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            kullanici_adi TEXT NOT NULL UNIQUE,
#            sifre TEXT NOT NULL,
#            son_giris_tarihi TEXT,
#            son_giris_saati TEXT
#        )
#    """)
#    conn.commit()
#    print("`kullanicilar` tablosu başarıyla oluşturuldu!")
#except sqlite3.Error as e:
#    print(f"Tablo oluşturulurken hata oluştu: {e}")
#
## `hammadde_maliyet` tablosunu oluştur
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS hammadde_maliyet (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            kullanici_id INTEGER NOT NULL,
#            maliyet_kalemi TEXT NOT NULL,
#            maliyet_tutari REAL NOT NULL,
#            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
#        )
#    """)
#    conn.commit()
#    print("`hammadde_maliyet` tablosu başarıyla oluşturuldu!")
#except sqlite3.Error as e:
#    print(f"Tablo oluşturulurken hata oluştu: {e}")
#
## `genel_maliyet` tablosunu oluştur
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS genel_maliyet (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            kullanici_id INTEGER NOT NULL,
#            maliyet_kalemi TEXT NOT NULL,
#            maliyet_tutari REAL NOT NULL,
#            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
#        )
#    """)
#    conn.commit()
#    print("`genel_maliyet` tablosu başarıyla oluşturuldu!")
#except sqlite3.Error as e:
#    print(f"Tablo oluşturulurken hata oluştu: {e}")
#
## `web_scraping_verileri` tablosunu oluştur
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS web_scraping_verileri (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            kullanici_id INTEGER NOT NULL,
#            baslik TEXT NOT NULL,
#            konu TEXT NOT NULL,
#            anahtar_kelime TEXT NOT NULL,
#            yeni_mi INTEGER DEFAULT 1,
#            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
#        )
#    """)
#    conn.commit()
#    print("`web_scraping_verileri` tablosu başarıyla oluşturuldu!")
#except sqlite3.Error as e:
#    print(f"Tablo oluşturulurken hata oluştu: {e}")
#
## `secenekler` tablosunu oluştur
#try:
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS secenekler (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            kelime TEXT NOT NULL,
#            kullanici_id INTEGER NOT NULL,
#            katsayi REAL NOT NULL,
#            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
#        )
#    """)
#    conn.commit()
#    print("`secenekler` tablosu başarıyla oluşturuldu!")
#except sqlite3.Error as e:
#    print(f"Tablo oluşturulurken hata oluştu: {e}")
#
## `web_scraping_verileri` tablosuna yeni sütun ekle
#try:
#    cursor.execute("ALTER TABLE web_scraping_verileri ADD COLUMN yeni_mi INTEGER DEFAULT 1;")
#    conn.commit()
#    print("`web_scraping_verileri` tablosuna yeni sütun başarıyla eklendi!")
#except sqlite3.Error as e:
#    print(f"Yeni sütun eklenirken hata oluştu: {e}")
#
## `web_scraping_verileri` tablosuna yeni sütunlar ekle
#try:
#    cursor.execute("ALTER TABLE web_scraping_verileri ADD COLUMN kullanici_adi TEXT;")
#    cursor.execute("ALTER TABLE web_scraping_verileri ADD COLUMN tarih_saat TEXT;")
#    conn.commit()
#    print("`web_scraping_verileri` tablosuna yeni sütunlar başarıyla eklendi!")
#except sqlite3.Error as e:
#    print(f"Yeni sütunlar eklenirken hata oluştu: {e}")
#
## Bağlantıyı kapat
#conn.close()

#try:
#    query = "SELECT * FROM hammadde_maliyet"
#    df = pd.read_sql_query(query, conn)
#    print(df)
#except sqlite3.Error as e:
#    print(f"Veritabanı hatası: {e}")
#
#
#try:
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM kullanicilar")
#    rows = cursor.fetchall()
#
#    data = np.array(rows)
#    print(data)
#
#except sqlite3.Error as e:
#    print(f"Veritabanı hatası: {e}")

try:
    tables = ["hammadde_maliyet", "genel_maliyet", "web_scraping_verileri", "secenekler"]
    for table in tables:
        print(f"\nTablo: {table}")
        komut = f"SELECT * FROM {table}"
        df = pd.read_sql_query(komut, conn)
        print(df)

except sqlite3.Error as e:
    print(f"Veritabanı hatası: {e}")