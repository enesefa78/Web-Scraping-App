import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QStackedWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from hammaddemaliyet import HammaddeMaaliyetSayfasi  # Hammadde maliyet sayfasını ekledik
from datetime import datetime


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(850, 650)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.connectDB()
        self.createLoginPage()

    def connectDB(self):
        try:
            self.conn = sqlite3.connect("fiyatlandirma_tahmin.db")
            cursor = self.conn.cursor()

            # Veritabanı tablolarını oluştur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_adi TEXT NOT NULL UNIQUE,
                    sifre TEXT NOT NULL,
                    son_giris_tarihi TEXT,
                    son_giris_saati TEXT
                )
            """)
            self.conn.commit()
            print("Veritabanına başarıyla bağlanıldı!")
        except sqlite3.Error as e:
            print(f"Veritabanı bağlantısı hatası: {e}")

    def createLoginPage(self):
        login_page = QWidget()
        login_layout = QFormLayout()
        login_layout.setFormAlignment(Qt.AlignCenter)

        username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(200)
        password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setFixedWidth(200)
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Giriş")
        login_button.setFixedWidth(200)
        login_button.clicked.connect(self.checkLogin)

        register_button = QPushButton("Kayıt Ol")
        register_button.setFixedWidth(200)
        register_button.clicked.connect(self.createRegisterPage)

        login_layout.addRow("", username_label)
        login_layout.addRow("", self.username_input)
        login_layout.addRow("", password_label)
        login_layout.addRow("", self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)

        login_layout.addRow("", button_layout)

        login_page.setLayout(login_layout)
        self.stacked_widget.addWidget(login_page)

    def createRegisterPage(self):
        register_page = QWidget()
        register_layout = QFormLayout()
        register_layout.setFormAlignment(Qt.AlignCenter)

        username_label = QLabel("Kullanıcı Adı:")
        self.register_username_input = QLineEdit()
        self.register_username_input.setFixedWidth(200)
        password_label = QLabel("Şifre:")
        self.register_password_input = QLineEdit()
        self.register_password_input.setFixedWidth(200)
        self.register_password_input.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Kayıt Ol")
        register_button.setFixedWidth(200)
        register_button.clicked.connect(self.registerUser)

        back_button = QPushButton("Geri Dön")
        back_button.setFixedWidth(200)
        back_button.clicked.connect(self.createLoginPage)

        register_layout.addRow("", username_label)
        register_layout.addRow("", self.register_username_input)
        register_layout.addRow("", password_label)
        register_layout.addRow("", self.register_password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(register_button)
        button_layout.addWidget(back_button)

        register_layout.addRow("", button_layout)

        register_page.setLayout(register_layout)
        self.stacked_widget.addWidget(register_page)
        self.stacked_widget.setCurrentWidget(register_page)

    def registerUser(self):
        username = self.register_username_input.text()
        password = self.register_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (username, password))
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı! Giriş yapabilirsiniz.")
            self.createLoginPage()  # Kayıt sonrası giriş sayfasına dön
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten alınmış!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")

    def checkLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (username, password))
            user = cursor.fetchone()

            if user:
                self.openHammaddeMaliyet(user[0], username,self.conn)  # Hammadde maliyet sayfasına geçiş
            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def logUserLogin(self, user_id):
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now()
            login_date = current_time.strftime("%Y-%m-%d")
            login_time = current_time.strftime("%H:%M:%S")

            cursor.execute("""
                UPDATE kullanicilar
                SET son_giris_tarihi=?, son_giris_saati=?
                WHERE id=?
            """, (login_date, login_time, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Giriş kaydı eklenirken hata oluştu: {e}")

    def openHammaddeMaliyet(self, kullanici_id, username,conn):
        try:
            self.hammadde_maliyet = HammaddeMaaliyetSayfasi(kullanici_id, username,conn,)
            self.setCentralWidget(self.hammadde_maliyet)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")
            print(f"Bir hata oluştu: {e}")
            import traceback
            traceback.print_exc()

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
            print("Veritabanı bağlantısı kapatıldı.")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
