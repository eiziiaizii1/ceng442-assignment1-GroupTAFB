# ceng442-assignment1-GroupTAFB
## CENG442 Assignment 1 - Azerbaijani Text Preprocessing & Word Embeddings

**Group Members:**
* Talha Ubeydullah Gamga | 20050111078
* Aziz Önder | 22050141021
* Muhammed Fatih Asan | 23050151026
* Buğra Bildiren | 20050111022

---

## Proje Durumu ve Sonraki Adımlar
Bu belge, projenin mevcut durumunu ve bir sonraki aşamaya (Model Eğitimi) geçecek ekip üyeleri için talimatları içerir.

### 1. Aşama: Veri Ön İşleme (Data Preprocessing) - TAMAMLANDI
Bu aşama (Kişi 1 ve Kişi 2'nin sorumluluğu) başarıyla tamamlanmıştır.

**Neler Yapıldı?** Ödev PDF'inde (`CENG442_Assignment1_.pdf`) belirtilen 5 adet ham `.xlsx` veri seti (`data/` klasöründe) okundu ve aşağıdaki işlemlerden geçirildi:

* **Temel Temizlik:** Azerbaycancaya özel küçük harf dönüşümü (İ→i, I→ı), HTML etiketleri, URL, E-posta ve Sayı (`<NUM>`) temizliği yapıldı.
* **Özel Temizlik (`ozel_temizlik.py` kullanılarak):**
    * Metinler "news", "social", "reviews", "general" olarak etiketlendi.
    * "Reviews" alanı için Fiyat (`<PRICE>`) ve Puan (`<STARS_HIGH>`) etiketlemesi yapıldı.
    * Emojiler (`EMO_POS`, `EMO_NEG`) haritalandı.
    * Hashtag'ler (`#QarabagIsBack` → `qarabag is back`) ayrıştırıldı.
    * Olumsuzluk ekleri (`yox`, `deyil` vb.) `_NEG` ile etiketlendi.
* **Etiket Standardizasyonu:** 5 farklı dosyadaki tüm duygu etiketleri (Positive, negative, 0, 1, 0.5 vb.) standart `float` (0.0, 0.5, 1.0) formatına dönüştürüldü.
* **Çıktı (Deliverable #1):** Bu işlemler sonucunda, ödevin 1. teslimatı olan 5 adet temizlenmiş, iki sütunlu (`cleaned_text`, `sentiment_value`) Excel dosyası üretildi ve `clean_data/` klasörüne kaydedildi.

Bu sürecin tamamı `Notebook_ceng442_assignment1_GroupTAFB.ipynb` dosyasında adım adım görülebilir.

### 2. Aşama: Model Eğitimi (Word2Vec/FastText) - HAZIR
Proje, 2. aşama olan model eğitimine (Kişi 3'ün görevi) hazırdır.

**Yapılması Gerekenler (Sonraki Adımlar):** Bir sonraki arkadaşımızın bu noktadan devam etmesi için yapması gerekenler:

1.  **`clean_data/` Klasörünü Kullanmak:** Model eğitimi için kaynak olarak `data/` klasöründeki ham verileri *kullanmayın*. Eğitim için `clean_data/` klasöründeki 5 adet temizlenmiş `..._2col.xlsx` dosyasını okumanız gerekmektedir.
2.  **Corpus (Deliverable #2) Oluşturma:** Bu 5 temiz dosyayı okuyun ve PDF'teki (Bölüm 7.2 - `build_corpus_txt`) iskeleti kullanarak `corpus_all.txt` dosyasını oluşturun. (Not: Bu iskelet, `ozel_temizlik.py` dosyasındaki `add_domain_tag` fonksiyonunu da kullanır.)
3.  **Model (Deliverable #3) Eğitimi:** `corpus_all.txt` dosyasını kullanarak Word2Vec ve FastText modellerini (PDF Bölüm 8) eğitin ve `embeddings/` klasörüne kaydedin.
4.  **Değerlendirme:** Modelleri PDF'teki (Bölüm 9) metriklere göre (Kapsam, Benzerlik, En Yakın Komşular) karşılaştırın.

---

## Proje Kurulumu (Reproducibility)
Bu projenin (ve `Notebook_...ipynb` dosyasının) çalıştırılabilmesi için gerekli adımlar:

1.  Projeyi klonlayın:
    ```bash
    git clone [https://github.com/GroupTAFB/ceng442-assignment1-GroupTAFB.git](https://github.com/GroupTAFB/ceng442-assignment1-GroupTAFB.git)
    cd ceng442-assignment1-GroupTAFB
    ```
2.  Bir sanal ortam (virtual environment) oluşturun ve aktive edin:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Gerekli tüm bağımlılıkları (`requirements.txt` dosyasından) yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4.  (Eğer Jupyter kullanıyorsanız) Sanal ortamı Jupyter'e tanıtın:
    ```bash
    python -m ipykernel install --user --name=venv
    ```
5.  Jupyter Notebook'u başlatın ve `Kernel > Change kernel` menüsünden `ceng442-venv` seçeneğini seçin.
    ```bash
    jupyter notebook
    ```

---

## Google Colab için Kurulum
Eğer model eğitimini (2. Aşama) Google Colab üzerinde yapmak isterseniz, Colab notebook'unuzdaki **ilk hücrede** şu komutları çalıştırmanız yeterlidir:

```python
# 1. Projeyi (içindeki clean_data/ ve ozel_temizlik.py dahil) klonla
!git clone [https://github.com/GroupTAFB/ceng442-assignment1-GroupTAFB.git](https://github.com/GroupTAFB/ceng442-assignment1-GroupTAFB.git)

# 2. Proje klasörüne gir
%cd ceng442-assignment1-GroupTAFB

# 3. Gerekli kütüphaneleri kur
!pip install -r requirements.txt

# 4. Artık 'clean_data/' klasöründeki dosyaları okuyabilir
#    ve 'ozel_temizlik.py' dosyasını import edebilirsiniz.
# import ozel_temizlik
# pd.read_excel("clean_data/test_1_2col.xlsx")