# HyperLogLog: Büyük Veri Analitiğinde Kardinalite Tahmini

Bu proje, "Büyük Veri Analitiği" dersi kapsamında olasılıksal veri yapılarını incelemek amacıyla geliştirilmiştir. Küme büyüklüğü tahmini (Cardinality Estimation) problemi için endüstri standardı olan HyperLogLog (HLL) algoritması, hiçbir harici kütüphane kullanılmadan temel matematiksel prensipleriyle Python üzerinde sıfırdan tasarlanmış ve analiz edilmiştir.

## 📌 Proje Özeti
Milyarlarca veriyi tek tek saymak bellek (RAM) açısından yüksek bir karmaşıklık yaratır. Bu proje, verinin hash'lenmiş istatistiksel dağılımını kullanarak bellek tüketimini minimize eden olasılıksal bir yaklaşım sunar.

### Temel Özellikler
* **Deterministik Hash:** `hashlib` kullanılarak MD5 algoritması ile verilerin kovalara homojen dağıtılması.
* **Kovalama (Bucketing):** Bit seviyesinde işlemlerle verilerin ilgili kovalara (register) atanması.
* **Harmonik Ortalama:** Uç değerlerin (outliers) sapma yaratmasını önleyen matematiksel tahmin modeli.
* **Düzeltme Faktörleri:** Küçük (Linear Counting) ve büyük veri setleri (Hash Collision önleme) için adaptif düzeltmeler.
* **Merge (Birleştirme):** İki farklı HLL yapısının veri kaybı olmadan birleştirilebilmesi.

## 🤖 Geliştirme Ortamı ve Agentic Kodlama
Bu proje **Agentic Kodlama (Ajanlı Geliştirme)** prensipleriyle geliştirilmiştir. 
* **IDE:** Visual Studio Code
* **Dil:** Python 3.x
* **Yapay Zeka Modeli:** Gemini (Ajan olarak konumlandırıldı)
* **Yöntem:** Yapay zeka, salt bir kod üretici olarak değil; mimari kararların alındığı, modüllerin (hash, bucket, merge) iteratif olarak parçalara bölünüp test edildiği analitik bir mühendislik asistanı olarak kullanılmıştır.

## 🚀 Kurulum ve Kullanım
Proje, Python'ın standart kütüphaneleri (`math`, `hashlib`) dışında hiçbir bağımlılık gerektirmez.

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/A-GorkemDogan/HyperLogLog

2. İlgili dizine giderek Python betiğini çalıştırın:
    ```bash
   python hyperloglog.py

Not: Kodu çalıştırdığınızda, algoritmanın hata sınırlarını ve birleştirme (merge) yeteneğini kanıtlayan iki adet test senaryosu otomatik olarak konsola yazdırılacaktır.
