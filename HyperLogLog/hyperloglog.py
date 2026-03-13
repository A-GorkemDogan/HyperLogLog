import hashlib
import math

class HyperLogLog:
    def __init__(self, b):
        """
        HyperLogLog veri yapısını başlatır.
        :param b: Kova (bucket) sayısını belirleyen bit sayısı. Genellikle 4 <= b <= 16 arasındadır.
        """
        if not (4 <= b <= 16):
            raise ValueError("b değeri 4 ile 16 arasında olmalıdır.")
            
        self.b = b
        self.m = 1 << b  # Kova sayısı: 2^b
        self.registers = [0] * self.m # Her kova için başlangıç değeri 0

        # Harmonik ortalama hesabında kullanılacak düzeltme sabiti (alpha_m)
        if self.m == 16:
            self.alpha_m = 0.673
        elif self.m == 32:
            self.alpha_m = 0.697
        elif self.m == 64:
            self.alpha_m = 0.709
        else:
            self.alpha_m = 0.7213 / (1.0 + 1.079 / self.m)

    def _get_hash(self, item):
        """
        Verilen eleman için 32-bit deterministik bir hash üretir.
        """
        hash_hex = hashlib.md5(str(item).encode('utf-8')).hexdigest()
        return int(hash_hex[:8], 16)

    def _get_rho(self, w):
        """
        w (geri kalan bitler) içindeki en soldaki (leading) '1' bitinin pozisyonunu bulur.
        Yani ardışık sıfır sayısı + 1 döner.
        """
        bit_length = 32 - self.b
        binary_str = bin(w)[2:].zfill(bit_length)
        
        try:
            return binary_str.index('1') + 1
        except ValueError:
            return bit_length + 1

    def add(self, item):
        """
        Kümeye yeni bir eleman ekler ve register durumunu günceller.
        """
        x = self._get_hash(item)
        binary_x = bin(x)[2:].zfill(32)
        
        j_str = binary_x[:self.b]
        j = int(j_str, 2)
        
        w_str = binary_x[self.b:]
        w = int(w_str, 2)
        
        self.registers[j] = max(self.registers[j], self._get_rho(w))

    def count(self):
        """
        Register'lardaki mevcut duruma bakarak kümedeki eşsiz eleman sayısını (kardinaliteyi) tahmin eder.
        """
        # 1. Harmonik ortalamanın paydasını hesapla (Z)
        Z = sum(math.pow(2.0, -val) for val in self.registers)
        
        # 2. Ham tahmini (Raw Estimate) hesapla
        E = self.alpha_m * (self.m ** 2) / Z
        
        # 3. Düzeltme Faktörlerini (Correction Factors) Uygula
        
        # Küçük Veri Seti Düzeltmesi
        if E <= 2.5 * self.m:
            V = self.registers.count(0) # Boş kova sayısı
            if V > 0:
                E = self.m * math.log(self.m / V)
                
        # Büyük Veri Seti Düzeltmesi (32 bit hash için)
        elif E > (1 / 30.0) * (2 ** 32):
            E = -(2 ** 32) * math.log(1.0 - (E / (2 ** 32)))
            
        return int(E)
    
    def merge(self, other_hll):
        """
        Başka bir HyperLogLog nesnesini mevcut nesneyle birleştirir.
        :param other_hll: Birleştirilecek diğer HyperLogLog nesnesi.
        """
        # Güvenlik kontrolü: Her iki yapının kova sayısı (b değeri) aynı olmalıdır.
        if self.b != other_hll.b:
            raise ValueError("Sadece aynı 'b' (kova) değerine sahip HLL yapıları birleştirilebilir.")
            
        # Her bir register için, iki yapıdaki değerlerden maksimum olanı alıyoruz.
        for i in range(self.m):
            self.registers[i] = max(self.registers[i], other_hll.registers[i])

import random

def run_tests():
    # 1. Teorik Hata ve Gerçek Hata Karşılaştırması
    print("--- 1. HATA ANALİZİ TESTİ ---")
    b_value = 10  # m = 1024
    hll = HyperLogLog(b_value)
    
    actual_cardinality = 50000
    print(f"Gerçek Eşsiz Eleman Sayısı: {actual_cardinality}")
    
    # Kümeye 50.000 adet eşsiz sayı ekleyelim
    for i in range(actual_cardinality):
        hll.add(f"item_{i}")
        
    estimated_cardinality = hll.count()
    print(f"HLL Tahmini: {estimated_cardinality}")
    
    # Hata oranlarını hesaplayalım
    actual_error = abs(actual_cardinality - estimated_cardinality) / actual_cardinality
    theoretical_error = 1.04 / math.sqrt(hll.m)
    
    print(f"Gerçekleşen Hata Oranı: %{actual_error * 100:.2f}")
    print(f"Teorik Beklenen Hata:   ~%{theoretical_error * 100:.2f}")
    print("-" * 30)

    # 2. Merge (Birleştirme) Özelliği Testi
    print("\n--- 2. MERGE (BİRLEŞTİRME) TESTİ ---")
    hll_A = HyperLogLog(b_value)
    hll_B = HyperLogLog(b_value)
    
    # A kümesine 1'den 1000'e kadar olan sayıları ekle
    for i in range(1, 1001):
        hll_A.add(i)
        
    # B kümesine 500'den 1500'e kadar olan sayıları ekle 
    # (Ortak elemanlar var, toplam eşsiz eleman 1500 olmalı)
    for i in range(500, 1501):
        hll_B.add(i)
        
    print(f"A Kümesi Tahmini (1-1000): {hll_A.count()}")
    print(f"B Kümesi Tahmini (500-1500): {hll_B.count()}")
    
    # A ve B'yi birleştir
    hll_A.merge(hll_B)
    
    print(f"A ve B Birleşiminin Tahmini (Beklenen: ~1500): {hll_A.count()}")

if __name__ == "__main__":
    run_tests()