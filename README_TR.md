# DTMF Touch-Tone Sinyal Sentezleyici ve Spektral Kod Çözücü (DSP)

Bu proje, telekomünikasyon sistemlerinin temel yapı taşlarından biri olan Çift Tonlu Çoklu Frekans (DTMF - Dual-Tone Multi-Frequency) sinyalleşme protokolünün Ayrık Zamanlı Sinyal İşleme (DSP) algoritmalarıyla modellenmesini, sentezlenmesini ve çözümlenmesini (decoding) kapsamaktadır. Uygulama hem Python hem de MATLAB ortamlarında eşzamanlı olarak geliştirilmiştir.

---

## 1. Teorik Altyapı ve Matematiksel Model

Geleneksel tuş takımlarında (keypad) basılan her tuş, bir düşük frekans (satır) ve bir yüksek frekans (sütun) sinüzoidinin toplamı şeklinde ifade edilir. $8192text{ Hz}$ örnekleme frekansı ($F_s$) altında normalize edilmiş açısal frekanslar ($omega$) cinsinden ayrık zamanlı sinyal modeli

$$d_k[n] = sin(omega_{row} cdot n) + sin(omega_{col} cdot n)$$

Örneğin 5 tuşuna basıldığında üretilen kompozit sinyal
$$d_5[n] = sin(0.5906,n) + sin(1.0247,n)$$

### Frekans Grid Tablosu ($text{radörnek}$)

 Satır  Sütun  $omega_{col} = 0.9273$  $omega_{col} = 1.0247$  $omega_{col} = 1.1328$ 
 ---  ---  ---  --- 
 $omega_{row} = 0.5346$  1  2  3 
 $omega_{row} = 0.5906$  4  5  6 
 $omega_{row} = 0.6535$  7  8  9 
 $omega_{row} = 0.7217$    0  # 

---

## 2. Sektördeki Önemi ve Endüstriyel Kullanım Alanları

DTMF teknolojisi, telekomünikasyon tarihinin en dayanıklı bant-içi (in-band) sinyalleşme standartlarından biridir. Projenin endüstrideki karşılıkları şunlardır

1. Gürültüye Karşı Bağışıklık (Harmonik Koruma)
    Seçilen frekanslar matematiksel olarak birbirlerinin harmonikleri (tam katları) olmayacak şekilde optimize edilmiştir.
    Bu sayede insan sesi, hat gürültüsü veya hat distorsiyonları tuş tonu zannedilerek yanlış tetiklenmez (talk-off protection).

2. IVR (Interactive Voice Response) ve Bankacılık Sistemleri
    Müşteri hizmetlerinde İşlemler için 1'e, transfer için 2'ye basınız şeklinde çalışan tüm sesli yanıt ve santral mimarileri bu tonların spektral olarak çözümlenmesine dayanır.

3. Telsiz ve Kritik Haberleşme (PMRTETRA)
    Askeri ve sivil telsiz ağlarında bas-konuş (PTT) sistemlerinde telsizin kimliğini (ID) veya röle anahtarlamasını taşımak için DTMF kullanılır.

4. Gömülü Sistemler ve IoT
    Çok düşük işlemci gücü olan mikrodenetleyicilerde (ARM Cortex-M  STM32), analog ses hattı üzerinden veri aktarımı veya uzaktan kontrol komutları göndermek için hafif DTMF algoritmaları (örneğin Goertzel) tercih edilir.

---

## 3. Sistem Mimarisi ve Kod Yapısı

 Sinyal Üretimi (Synthesis) Tuş girdisine göre belirlenen satır ve sütun frekansları süperpozisyon prensibiyle toplanır.
 Frekans Analizi (DTFTFFT) 2048 noktalı FFT ile spektral sızıntı azaltılır ve yüksek frekans çözünürlüğü elde edilir.
 Kod Çözücü (Decoder) Düşük bant $[0.45, 0.80]text{ rad}$ ve yüksek bant $[0.85, 1.25]text{ rad}$ aralıklarında tepe tespiti (peak detection) yapılarak en yakın tuş matris koordinatlarına eşlenir.

---

## 4. Kurulum ve Çalıştırma

### Python
Gereksinimler `numpy`, `matplotlib`
```bash
pip install numpy matplotlib
python dtmf_analyzer.py