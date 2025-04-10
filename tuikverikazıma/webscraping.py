#import sys
#import sqlite3
#from PyQt5.QtWidgets import (
#    QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit,
#    QPushButton, QScrollArea, QWidget
#)
#from PyQt5.QtCore import Qt
#from datetime import datetime
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#
#class ProductCalculator(QMainWindow):
#    def __init__(self, kullanici_id=None):
#        super().__init__()
#        self.kullanici_id = kullanici_id
#        self.initUI()
#        self.conn = sqlite3.connect("fiyatlandirma_tahmin.db")
#        self.username_input = QLineEdit()
#        self.password_input = QLineEdit()
#
#    def initUI(self):
#        self.setWindowTitle("Ürün Hesaplama Arayüzü")
#        self.setFixedSize(850, 650)
#
#        self.hammadde_sayisi_label = QLabel("Kaç adet hammadde kullanacaksınız?")
#        self.hammadde_sayisi_input = QLineEdit()
#        self.hammadde_sayisi_button = QPushButton("Devam Et")
#        self.hammadde_sayisi_button.clicked.connect(self.createMaterialInputs)
#
#        self.central_widget = QWidget()
#        self.setCentralWidget(self.central_widget)
#
#        layout = QFormLayout()
#        layout.addWidget(self.hammadde_sayisi_label)
#        layout.addWidget(self.hammadde_sayisi_input)
#        layout.addWidget(self.hammadde_sayisi_button)
#
#        self.central_widget.setLayout(layout)
#
#    def createMaterialInputs(self):
#        try:
#            self.material_count = int(self.hammadde_sayisi_input.text())
#        except ValueError:
#            return  # Sayı girilmemişse işlemi yapma
#
#        self.material_inputs = []
#
#        central_layout = self.centralWidget().layout()
#        for widget in [self.hammadde_sayisi_label, self.hammadde_sayisi_input, self.hammadde_sayisi_button]:
#            central_layout.removeWidget(widget)
#            widget.deleteLater()
#
#        self.material_layout = QFormLayout()
#
#        self.total_product_label = QLabel("Toplam Üretilen Ürün Sayısını Giriniz")
#        self.total_product_input = QLineEdit()
#        self.material_layout.addRow(self.total_product_label, self.total_product_input)
#
#        for i in range(self.material_count):
#            self.material_layout.addRow(QLabel(f"Hammadde {i + 1} Bilgileri:"))
#
#            name_input = QLineEdit()
#            quantity_input = QLineEdit()
#            unit_input = QLineEdit()
#            price_input = QLineEdit()
#
#            self.material_inputs.append((name_input, quantity_input, unit_input, price_input))
#
#            self.material_layout.addRow("Hammadde İsmi:", name_input)
#            self.material_layout.addRow("Miktar:", quantity_input)
#            self.material_layout.addRow("Birim:", unit_input)
#            self.material_layout.addRow("Ürün Birim Fiyatı:", price_input)
#
#        self.calculate_button = QPushButton("Hesapla")
#        self.calculate_button.clicked.connect(self.calculateProductCost)
#        self.material_layout.addWidget(self.calculate_button)
#
#        self.nextPage_button = QPushButton("Sonraki Sayfa")
#        self.nextPage_button.clicked.connect(self.openNewPage)
#        self.material_layout.addWidget(self.nextPage_button)
#
#        scroll_widget = QWidget()
#        scroll_widget.setLayout(self.material_layout)
#
#        scroll_area = QScrollArea()
#        scroll_area.setWidgetResizable(True)
#        scroll_area.setWidget(scroll_widget)
#
#        central_layout.addWidget(scroll_area)
#
#    def checkLogin(self):
#        username = self.username_input.text()
#        password = self.password_input.text()
#
#        cursor = self.conn.cursor()
#        cursor.execute(
#            'SELECT id FROM kullanicilar WHERE kullanici_adi=? AND sifre=?',
#            (username, password)
#        )
#        user = cursor.fetchone()
#
#        if user:
#            self.kullanici_id = user[0]
#            # Update last login time
#            cursor.execute(
#                'UPDATE kullanicilar SET son_giris_tarihi=? WHERE id=?',
#                (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.kullanici_id)
#            )
#            self.conn.commit()
#            self.openProductCalculator()
#        else:
#            print("Giriş başarısız")
#
#    def calculateProductCost(self):
#        try:
#            total_cost = 0
#            cursor = self.conn.cursor()
#            insert_query = """
#                INSERT INTO urun_verileri (kullanici_id, hammadde_ismi, miktar, birim, birim_fiyat)
#                VALUES (?, ?, ?, ?, ?)
#            """
#
#            for name_input, quantity_input, unit_input, price_input in self.material_inputs:
#                name = name_input.text()
#                quantity = float(quantity_input.text())
#                unit = unit_input.text()
#                price = float(price_input.text())
#
#                total_cost += quantity * price
#
#                cursor.execute(insert_query, (self.kullanici_id, name, quantity, unit, price))
#            self.conn.commit()
#
#            result_label = QLabel(f"Ürün başı hammadde maliyeti: {total_cost:.2f} TL")
#            result_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
#            self.material_layout.addWidget(result_label)
#
#        except Exception as e:
#            print(f"Bir hata oluştu: {e}")
#            import traceback
#            traceback.print_exc()
#
#    def openNewPage(self):
#        from genelmaliyet import MaliyetHesaplamaUygulamasi  # Import moved here to avoid circular import
#        self.genelmaliyet = MaliyetHesaplamaUygulamasi()
#        self.setCentralWidget(self.genelmaliyet)
#
#    def web_scraping_yap(self, anahtar_kelime):
#        options = webdriver.ChromeOptions()
#        options.add_argument("--headless")  # Tarayıcıyı arka planda aç
#
#        # WebDriver Manager ile ChromeDriver'ı otomatik yönetin
#        service = Service(ChromeDriverManager().install())
#        driver = webdriver.Chrome(service=service, options=options)
#
#        try:
#            driver.get("https://www.tuik.gov.tr/")
#            # Web scraping işlemleri burada devam eder...
#        finally:
#            driver.quit()
#
#
#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    window = ProductCalculator()
#    window.show()
#    sys.exit(app.exec_())///
