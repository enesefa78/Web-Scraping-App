import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QWidget, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
from genelmaliyet import GenelMaliyetHesaplamaSayfasi

class HammaddeMaaliyetSayfasi(QMainWindow):
    def __init__(self, kullanici_id, username,conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username  # Kullanıcı adını sakla

        # SQLite veritabanı bağlantısı
        self.conn = conn

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hammadde Maliyet Hesaplama")
        self.setFixedSize(850, 650)

        layout = QVBoxLayout()

        # Kullanıcı bilgilerini göster
        user_info_label = QLabel(f"Kullanıcı ID: {self.kullanici_id}, Kullanıcı Adı: {self.username}")
        layout.addWidget(user_info_label)

        # Hammadde sayısı giriş alanı
        self.hammadde_sayisi_label = QLabel("Kaç adet hammadde kullanacaksınız?")
        self.hammadde_sayisi_input = QLineEdit()
        self.hammadde_sayisi_button = QPushButton("Devam Et")
        self.hammadde_sayisi_button.clicked.connect(self.createMaterialInputs)

        for widget in [self.hammadde_sayisi_label, self.hammadde_sayisi_input, self.hammadde_sayisi_button]:
            widget.setFixedHeight(30)
            widget.setFixedWidth(300)

        layout.addWidget(self.hammadde_sayisi_label)
        layout.addWidget(self.hammadde_sayisi_input)
        layout.addWidget(self.hammadde_sayisi_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def createMaterialInputs(self):
        try:
            self.material_count = int(self.hammadde_sayisi_input.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayı giriniz!")
            return

        self.material_inputs = []
        layout = self.centralWidget().layout()

        # Giriş formu bileşenlerini kaldır
        for widget in [self.hammadde_sayisi_label, self.hammadde_sayisi_input, self.hammadde_sayisi_button]:
            layout.removeWidget(widget)
            widget.deleteLater()

        self.material_layout = QFormLayout()

        # Genel ürün sayısı girişi
        self.total_product_label = QLabel("Toplam Üretilen Ürün Sayısını Giriniz")
        self.total_product_input = QLineEdit()
        self.material_layout.addRow(self.total_product_label, self.total_product_input)

        # Hammadde girişlerini oluştur
        for i in range(self.material_count):
            name_input = QLineEdit()
            quantity_input = QLineEdit()
            unit_input = QLineEdit()
            price_input = QLineEdit()

            self.material_inputs.append((name_input, quantity_input, unit_input, price_input))

            self.material_layout.addRow(f"Hammadde {i + 1} İsmi:", name_input)
            self.material_layout.addRow(f"Hammadde {i + 1} Miktarı:", quantity_input)
            self.material_layout.addRow(f"Hammadde {i + 1} Birimi:", unit_input)
            self.material_layout.addRow(f"Hammadde {i + 1} Birim Fiyatı:", price_input)

        # Hesapla ve Sonraki Sayfa butonları
        self.calculate_button = QPushButton("Hesapla")
        self.calculate_button.clicked.connect(self.calculateProductCost)

        self.nextPage_button = QPushButton("Sonraki Sayfa")
        self.nextPage_button.clicked.connect(self.openNextPage)

        self.material_layout.addRow(self.calculate_button)
        self.material_layout.addRow(self.nextPage_button)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.material_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        layout.addWidget(scroll_area)

    def calculateProductCost(self):
        try:
            material_cost = 0
            cursor = self.conn.cursor()
            insert_query = """
                INSERT INTO urun_verileri (kullanici_id, hammadde_ismi, miktar, birim, birim_fiyat)
                VALUES (?, ?, ?, ?, ?)
            """

            for name_input, quantity_input, unit_input, price_input in self.material_inputs:
                name = name_input.text()
                quantity = float(quantity_input.text())
                unit = unit_input.text()
                price = float(price_input.text())
                material_cost += quantity * price

                cursor.execute(insert_query, (self.kullanici_id, name, quantity, unit, price))
                self.conn.commit()

            QMessageBox.information(self, "Sonuç", f"Ürün başı hammadde maliyeti: {material_cost:.2f} TL")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doğru bir şekilde doldurun!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")
            import traceback
            traceback.print_exc()

    def openNextPage(self):
        try:
            self.genel_maliyet = GenelMaliyetHesaplamaSayfasi(self.kullanici_id, self.username, self.conn)
            self.genel_maliyet.show()
            self.close()  # Hammadde Maliyet Sayfasını kapat
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

class GenelMaliyet(QWidget):
    def __init__(self, kullanici_id, username, conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username
        self.conn = conn  # Veritabanı bağlantısını al
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hammadde Maliyet")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.maliyet_input = QLineEdit()
        layout.addWidget(QLabel("Hammadde Maliyeti:"))
        layout.addWidget(self.maliyet_input)

        save_button = QPushButton("Kaydet ve İlerle")
        save_button.clicked.connect(self.saveAndNext)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def saveAndNext(self):
        try:
            maliyet = float(self.maliyet_input.text())
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO hammadde_maliyet (kullanici_id, maliyet_kalemi, maliyet_tutari) VALUES (?, ?, ?)",
                           (self.kullanici_id, "Hammadde", maliyet))
            self.conn.commit()
            self.openGenelMaliyet()
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir maliyet girin!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def openGenelMaliyet(self):
        self.genel_maliyet = GenelMaliyetHesaplamaSayfasi(self.kullanici_id, self.username, self.conn)
        self.genel_maliyet.show()
        self.close()  # Hammadde Maliyet Sayfasını kapat

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Test için örnek kullanıcı ID'si ve kullanıcı adı ile başlatılıyor
    kullanici_id = 1  # Örnek kullanıcı ID'si
    username = "test_user"

    # SQLite veritabanı bağlantısını oluştur
    conn = sqlite3.connect("fiyatlandirma_tahmin.db")

    # HammaddeMaaliyetSayfasi sınıfını başlatırken conn parametresini ekleyin
    window = HammaddeMaaliyetSayfasi(kullanici_id, username, conn)
    window.show()

    sys.exit(app.exec_())
