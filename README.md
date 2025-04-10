TUİK Veri Kazıma ve Maliyet Hesaplama Uygulaması
Bu proje, TUİK (Türkiye İstatistik Kurumu) web sitesinden veri kazıma işlemleri yaparak verileri SQLite veritabanına kaydeden ve hammadde maliyet hesaplamaları gerçekleştiren bir PyQt5 uygulamasıdır. Uygulama, kullanıcıların maliyet hesaplamalarını kolaylaştırmak ve verileri düzenli bir şekilde saklamak için tasarlanmıştır.

Özellikler
Hammadde Maliyet Hesaplama:

Kullanıcı, hammadde bilgilerini (isim, miktar, birim, birim fiyat) girerek ürün başına maliyet hesaplayabilir.
Veriler SQLite veritabanına kaydedilir.
Genel Maliyet Hesaplama:

Kullanıcı, genel maliyet bilgilerini girerek toplam maliyet hesaplamalarını yapabilir.
Veriler veritabanına kaydedilir.
Web Scraping:

TUİK web sitesinden belirli anahtar kelimelerle veri kazıma işlemi yapılır.
Çekilen veriler (başlık, içerik, tarih) SQLite veritabanına kaydedilir.
Sonuç Görüntüleme:

Kullanıcı, tüm verileri bir tablo halinde görüntüleyebilir.
Veriler yeniden eskiye sıralanır.
Kullanılan Teknolojiler
Python 3.x
PyQt5: Masaüstü uygulama arayüzü için.
SQLite: Veritabanı yönetimi için.
Selenium: TUİK web sitesinden veri kazıma işlemleri için.
Pandas: Verileri analiz etmek ve tablo formatında düzenlemek için.
BeautifulSoup: HTML verilerini işlemek için.
Kurulum
1. Gerekli Bağımlılıkları Yükleyin
Proje için gerekli bağımlılıkları yüklemek için aşağıdaki komutu çalıştırın:

requirements.txt dosyasının içeriği şu şekilde olabilir:

2. ChromeDriver'ı İndirin
Selenium'un çalışması için ChromeDriver gereklidir. Aşağıdaki adımları izleyin:

ChromeDriver sayfasına gidin.
Kullandığınız Chrome sürümüne uygun olan ChromeDriver'ı indirin.
İndirdiğiniz dosyayı proje klasörüne veya PATH'e ekleyin.
Kullanım
1. Uygulamayı Başlatın
Aşağıdaki komutla uygulamayı çalıştırabilirsiniz:

2. Hammadde Maliyet Hesaplama
Uygulama açıldığında, kullanıcı ID'si ve kullanıcı adı bilgileri görüntülenir.
Kullanıcı, kaç adet hammadde kullanacağını girer ve "Devam Et" butonuna tıklar.
Hammadde bilgilerini (isim, miktar, birim, birim fiyat) girer ve "Hesapla" butonuna tıklar.
Ürün başına maliyet hesaplanır ve veritabanına kaydedilir.
3. Genel Maliyet Hesaplama
Hammadde maliyet hesaplama işlemi tamamlandıktan sonra, kullanıcı genel maliyet bilgilerini girer.
"Kaydet ve İlerle" butonuna tıklayarak verileri kaydeder ve bir sonraki sayfaya geçer.
4. Web Scraping
Kullanıcı, TUİK web sitesinden veri kazıma işlemi yapmak için bir anahtar kelime girer.
"Veri Çek" butonuna tıklayarak TUİK web sitesinden veriler çekilir ve veritabanına kaydedilir.
5. Verileri Görüntüleme
Kullanıcı, tüm verileri bir tablo halinde görüntüleyebilir.
Veriler yeniden eskiye sıralanır.
Veritabanı Yapısı
1. hammadde_maliyet Tablosu
Sütun Adı	Veri Tipi	Açıklama
id	INTEGER	Otomatik artan birincil anahtar.
kullanici_id	INTEGER	Kullanıcı ID'si.
maliyet_kalemi	TEXT	Hammadde kalemi adı.
maliyet_tutari	REAL	Hammadde maliyet tutarı.
2. genel_maliyet Tablosu
Sütun Adı	Veri Tipi	Açıklama
id	INTEGER	Otomatik artan birincil anahtar.
kullanici_id	INTEGER	Kullanıcı ID'si.
maliyet_kalemi	TEXT	Genel maliyet kalemi adı.
maliyet_tutari	REAL	Genel maliyet tutarı.
3. web_scraping_verileri Tablosu
Sütun Adı	Veri Tipi	Açıklama
id	INTEGER	Otomatik artan birincil anahtar.
kullanici_id	INTEGER	Kullanıcı ID'si.
baslik	TEXT	Çekilen verinin başlığı.
konu	TEXT	Çekilen verinin içeriği.
anahtar_kelime	TEXT	Kullanılan anahtar kelime.
tarih_saat	TEXT	Verinin çekildiği tarih ve saat.
Hata Ayıklama
1. Veritabanı Hataları
Eğer veriler kaydedilmiyorsa, self.conn.commit() çağrısının eksik olup olmadığını kontrol edin.
Veritabanı bağlantısının doğru bir şekilde yapıldığından emin olun.
2. Web Scraping Hataları
ChromeDriver'ın doğru bir şekilde yüklendiğinden ve PATH'e eklendiğinden emin olun.
TUİK web sitesindeki değişiklikler nedeniyle elementlerin ID'leri değişmiş olabilir. Bu durumda, selenium kodunu güncelleyin.
Geliştirme ve Katkı
Bu projeyi geliştirmek veya katkıda bulunmak isterseniz:

Bu projeyi forklayın.
Yeni bir dal (branch) oluşturun:
Değişikliklerinizi yapın ve commit edin:
Değişikliklerinizi GitHub'a gönderin:
Bir Pull Request oluşturun.
Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.

