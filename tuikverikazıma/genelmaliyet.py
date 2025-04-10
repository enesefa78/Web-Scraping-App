import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow
)
from sayfa4 import AnahtarKelimeUygulamasi  # Sayfa 4'ü ekledik


class GenelMaliyetHesaplamaSayfasi(QWidget):
    def __init__(self, kullanici_id, username, conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username  # Kullanıcı adını sakla
        self.conn = conn  # Veritabanı bağlantısını al
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Genel Maliyet Hesaplama")
        self.setFixedSize(850, 650)

        layout = QVBoxLayout()

        # Kullanıcı bilgilerini göster
        user_info_label = QLabel(f"Kullanıcı ID: {self.kullanici_id}, Kullanıcı Adı: {self.username}")
        layout.addWidget(user_info_label)

        # Genel maliyet giriş alanları
        self.inputs = {}
        maliyet_kalemleri = [
            "Enerji Maliyeti", "İşgücü Maliyeti", "Lojistik Maliyeti",
            "Paketleme Maliyeti", "Pazarlama ve Reklam Maliyeti", "Diğer Maliyetler"
        ]

        for kalem in maliyet_kalemleri:
            label = QLabel(f"{kalem}:")
            input_field = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.inputs[kalem] = input_field

        # Hesapla butonu
        hesapla_button = QPushButton("Hesapla")
        hesapla_button.clicked.connect(self.hesapla_maliyet)
        layout.addWidget(hesapla_button)

        # Sonraki sayfa butonu
        next_page_button = QPushButton("Sonraki Sayfa")
        next_page_button.clicked.connect(self.openNextPage)
        layout.addWidget(next_page_button)

        # Sonuç etiketi
        self.sonuc_label = QLabel("")
        layout.addWidget(self.sonuc_label)

        self.setLayout(layout)

    def hesapla_maliyet(self):
        try:
            toplam_maliyet = 0
            cursor = self.conn.cursor()
            insert_query = """
                INSERT INTO maliyet_verileri (kullanici_id, maliyet_kalemi, maliyet_tutari)
                VALUES (?, ?, ?)
            """

            for kalem, input_field in self.inputs.items():
                maliyet_tutari = float(input_field.text())
                toplam_maliyet += maliyet_tutari

                # Veritabanına maliyet kalemlerini kaydet
                cursor.execute(insert_query, (self.kullanici_id, kalem, maliyet_tutari))
            self.conn.commit()

            self.sonuc_label.setText(f"Toplam Maliyet: {toplam_maliyet:.2f} TL")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları sayısal değerle doldurun!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            import traceback
            traceback.print_exc()

    def openNextPage(self):
        from sayfa4 import AnahtarKelimeUygulamasi
        self.sayfa4 = AnahtarKelimeUygulamasi(self.kullanici_id, self.username, self.conn)
        self.sayfa4.show()
        self.close()


class GenelMaliyet(QWidget):
    def __init__(self, kullanici_id, username, conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username
        self.conn = conn  # Veritabanı bağlantısını al
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Genel Maliyet")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.maliyet_input = QLineEdit()
        layout.addWidget(QLabel("Genel Maliyet:"))
        layout.addWidget(self.maliyet_input)

        save_button = QPushButton("Kaydet ve İlerle")
        save_button.clicked.connect(self.saveAndNext)
        layout.addWidget(save_button)

        self.setLayout(layout)  # QWidget için setLayout kullanımı

    def saveAndNext(self):
        try:
            maliyet = float(self.maliyet_input.text())
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO genel_maliyet (kullanici_id, maliyet_kalemi, maliyet_tutari) VALUES (?, ?, ?)",
                           (self.kullanici_id, "Genel", maliyet))
            self.conn.commit()
            self.openNextPage()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir maliyet girin!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def openNextPage(self):
        from sayfa4 import AnahtarKelimeUygulamasi
        self.sayfa4 = AnahtarKelimeUygulamasi(self.kullanici_id, self.username, self.conn)
        self.sayfa4.show()
        self.close()  # Genel Maliyet Sayfasını kapat


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Test için örnek kullanıcı ID'si ve kullanıcı adı ile başlatılıyor
    conn = sqlite3.connect("fiyatlandirma_tahmin.db")
    kullanici_id = 1  # Örnek kullanıcı ID'si
    username = "test_user"
    window = AnahtarKelimeUygulamasi(kullanici_id, username, conn)
    window.show()

    sys.exit(app.exec_())
