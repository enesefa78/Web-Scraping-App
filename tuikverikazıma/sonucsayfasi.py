import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)


class SonucSayfasi(QWidget):
    def __init__(self, kullanici_id, username, conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username
        self.conn = conn  # Veritabanı bağlantısını al
        self.initUI()
        self.load_data()  # Tabloyu otomatik olarak doldur

    def initUI(self):
        self.setWindowTitle("Sonuç Sayfası")
        self.setFixedSize(850, 650)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Başlık", "Konu", "Anahtar Kelime", "Durum"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT baslik, konu, anahtar_kelime, kullanici_adi, tarih_saat
                FROM web_scraping_verileri
                WHERE kullanici_id = ?
                ORDER BY tarih_saat DESC  -- Verileri yeniden eskiye sıralar
            """, (self.kullanici_id,))
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Test için örnek kullanıcı ID'si ve kullanıcı adı ile başlatılıyor
    kullanici_id = 1  # Örnek kullanıcı ID'si
    username = "test_user"
    conn = sqlite3.connect("fiyatlandirma_tahmin.db")
    window = SonucSayfasi(kullanici_id, username, conn)
    window.show()

    sys.exit(app.exec_())