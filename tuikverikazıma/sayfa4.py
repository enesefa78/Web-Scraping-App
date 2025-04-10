from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QMessageBox, QSpinBox,
    QHBoxLayout, QLineEdit, QProgressDialog, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt  # Qt modülünü ekleyin
from selenium.webdriver.chrome.service import Service  # Service sınıfını ekleyin
from sonucsayfasi import SonucSayfasi
from datetime import datetime


class AnahtarKelimeUygulamasi(QMainWindow):
    def __init__(self, kullanici_id, username, conn):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.username = username
        self.conn = conn  # Veritabanı bağlantısını al

        # Kullanıcının son giriş tarihini ve saatini veritabanından al
        self.login_date, self.login_time = self.get_last_login_info()

        self.initUI()

    def get_last_login_info(self):
        """Kullanıcının son giriş tarihini ve saatini veritabanından alır."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT son_giris_tarihi, son_giris_saati
                FROM kullanicilar
                WHERE id = ?
            """, (self.kullanici_id,))
            result = cursor.fetchone()
            return result if result else (None, None)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
            return None, None

    def initUI(self):
        self.setWindowTitle("Anahtar Kelime Uygulaması")
        self.setFixedSize(850, 650)

        layout = QVBoxLayout()

        # Kullanıcı giriş bilgilerini göster
        if self.login_date and self.login_time:
            login_info_label = QLabel(f"Giriş Tarihi: {self.login_date}, Giriş Saati: {self.login_time}")
            layout.addWidget(login_info_label)

        # Kullanıcı bilgilerini göster
        user_info_label = QLabel(f"Kullanıcı ID: {self.kullanici_id}, Kullanıcı Adı: {self.username}")
        layout.addWidget(user_info_label)

        # Başlık etiketi
        label = QLabel(
            "Ürününüzün fiyatlandırmasında etkili faktörler içeren anahtar kelimeleri seçin ve her biri için katsayı girin:"
        )
        layout.addWidget(label)

        # Anahtar kelime listesi
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)

        anahtar_kelimeler = [
            "Borsa", "Enflasyon", "Döviz Kuru", "Altın",
            "İstihdam", "Enerji", "Global Haberler"
        ]
        self.list_widget.addItems(anahtar_kelimeler)

        # Katsayı giriş alanları
        self.katsayi_inputs = {}
        for kelime in anahtar_kelimeler:
            kelime_layout = QHBoxLayout()
            kelime_label = QLabel(kelime)
            spin_box = QSpinBox()
            kelime_layout.addWidget(kelime_label)
            kelime_layout.addWidget(spin_box)
            layout.addLayout(kelime_layout)
            self.katsayi_inputs[kelime] = spin_box

        # Yeni anahtar kelime girişi
        self.anahtar_kelime_input = QLineEdit()
        self.anahtar_kelime_input.setPlaceholderText("Yeni anahtar kelime girin...")
        layout.addWidget(self.anahtar_kelime_input)

        # Ara butonu
        self.ara_button = QPushButton("Ara")
        self.ara_button.clicked.connect(self.ara)
        layout.addWidget(self.ara_button)

        # Sonuç sayfasına geçiş butonu
        sonuc_button = QPushButton("Sonuç Sayfasına Geç")
        sonuc_button.clicked.connect(self.openSonucSayfasi)
        layout.addWidget(sonuc_button)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

    def connect_to_database(self):
        """SQLite veritabanına bağlanır ve gerekli tabloları oluşturur."""
        conn = sqlite3.connect("fiyatlandirma_tahmin.db")
        cursor = conn.cursor()

        # Tabloları oluştur
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secenekler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kelime TEXT NOT NULL,
                kullanici_id INTEGER NOT NULL,
                katsayi REAL NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_scraping_verileri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                baslik TEXT NOT NULL,
                konu TEXT NOT NULL,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS son_giris_bilgileri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL
            )
        """)
        conn.commit()
        return conn

    def get_latest_user_id(self):
        """Son giriş yapan kullanıcının ID'sini alır."""
        try:
            cursor = self.conn.cursor()  # self.db yerine self.conn kullanılıyor
            cursor.execute("""
                SELECT kullanici_id FROM son_giris_bilgileri
                WHERE id = (SELECT MAX(id) FROM son_giris_bilgileri) LIMIT 1
            """)
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
            return None

    def ara(self):
        secilenler = [item.text() for item in self.list_widget.selectedItems()]
        ek_kelime = self.anahtar_kelime_input.text().strip()

        if ek_kelime:
            secilenler.append(ek_kelime)

        if not secilenler:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir anahtar kelime seçin veya giriş yapın.")
            return

        gosterilecek_metin = "Seçilen Anahtar Kelimeler ve Katsayıları:\n"
        for kelime in secilenler:
            katsayi = self.katsayi_inputs.get(kelime, QSpinBox()).value()
            gosterilecek_metin += f"{kelime}: {katsayi}\n"

        QMessageBox.information(self, "Seçilen Anahtar Kelimeler ve Katsayılar", gosterilecek_metin)

        kullanici_id = self.get_latest_user_id()
        if kullanici_id:
            self.kelimeleri_seceneklere_kaydet(secilenler, kullanici_id)

        for kelime in secilenler:
            self.web_scraping_yap(kelime)

    def kelimeleri_seceneklere_kaydet(self, kelimeler, kullanici_id):
        """Seçilen anahtar kelimeleri ve katsayıları veritabanına kaydeder."""
        try:
            cursor = self.conn.cursor()  # self.db yerine self.conn kullanılıyor
            cursor.execute("DELETE FROM secenekler WHERE kullanici_id = ?", (kullanici_id,))
            insert_query = "INSERT INTO secenekler (kelime, kullanici_id, katsayi) VALUES (?, ?, ?)"

            for kelime in kelimeler:
                katsayi = self.katsayi_inputs.get(kelime, QSpinBox()).value()
                cursor.execute(insert_query, (kelime, kullanici_id, katsayi))

            self.conn.commit()
            cursor.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def web_scraping_yap(self, anahtar_kelime):
        chrome_path = "C:/Users/sefae/OneDrive/Masaüstü/projelerim/chromedriver-win64/chromedriver.exe"  # ChromeDriver'ın tam yolu
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırmak için (isteğe bağlı)
        options.add_argument("--ignore-certificate-errors")  # SSL hatalarını yoksay
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Kullanıcı aracısı

        # Yükleniyor simgesi
        progress_dialog = QProgressDialog("Veriler çekiliyor, lütfen bekleyin...", None, 0, 0, self)
        progress_dialog.setWindowTitle("Yükleniyor")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Service sınıfını kullanarak ChromeDriver'ı başlatın
        service = Service(chrome_path)
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get("https://www.tuik.gov.tr/")
            wait = WebDriverWait(driver, 10)
            search_input = wait.until(EC.presence_of_element_located((By.ID, "id_elastic_search_param")))
            search_input.send_keys(anahtar_kelime)
            search_input.send_keys(Keys.RETURN)

            wait.until(EC.presence_of_element_located((By.ID, "bultenTable")))
            html = driver.find_element(By.ID, "bultenTable").get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            titles = soup.select('a[style="color: #4e86d7; font-weight: bold;"]')
            contents = soup.select('p.text-secondary.pt-2[style="font-size: 1.5rem"]')

            cursor = self.conn.cursor()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Tarih ve saat bilgisi

            for title, content in zip(titles, contents):
                cursor.execute("""
                    INSERT INTO web_scraping_verileri (kullanici_id, baslik, konu, anahtar_kelime, kullanici_adi, tarih_saat)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.kullanici_id, title.text.strip(), content.text.strip(), anahtar_kelime, self.username, current_time))

            self.conn.commit()
            cursor.close()

            QMessageBox.information(self, "Başarılı", "Veriler başarıyla çekildi ve kaydedildi!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Web scraping hatası: {e}")
        finally:
            driver.quit()
            progress_dialog.close()  # Yükleniyor simgesini kapat

    def openSonucSayfasi(self):
        try:
            self.sonuc_sayfasi = SonucSayfasi(self.kullanici_id, self.username, self.conn)
            self.sonuc_sayfasi.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


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
        self.table.setColumnCount(5)  # Sütun sayısını artırdık
        self.table.setHorizontalHeaderLabels(["Başlık", "Konu", "Anahtar Kelime", "Kullanıcı", "Tarih ve Saat"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT baslik, konu, anahtar_kelime, kullanici_adi, tarih_saat
                FROM web_scraping_verileri
                WHERE kullanici_id = ?
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
    conn = sqlite3.connect("fiyatlandirma_tahmin.db")
    pencere = AnahtarKelimeUygulamasi(kullanici_id=1, username="test_user", conn=conn)  # Örnek kullanıcı ID'si ve kullanıcı adı
    pencere.show()
    sys.exit(app.exec_())
