# LOG Eksperimen EXP-002: Analisis Overlap N-Gram

**Tanggal:** 29 Januari 2026
**Status:** Completed
**Peneliti:** Gemini Agent

## 1. Tujuan
Memvalidasi keabsahan skor BLEU (~60) pada model NLLB baseline. Terdapat kecurigaan bahwa skor tinggi disebabkan oleh memorisasi frasa karena dataset yang kecil, bukan kemampuan generalisasi bahasa.

## 2. Metodologi
Menggunakan skrip `script.py` untuk menghitung overlap N-Gram (1-4) antara file `train.csv` dan `test.csv` pada kolom Source (Indonesia) dan Target (Sekar).

## 3. Hasil Temuan
Analisis menunjukkan tingkat overlap yang sangat tinggi:
*   **1-Gram (Kata):** 97% overlap.
*   **4-Gram (Frasa Panjang):** **61.17%** (Indonesia) dan **56.71%** (Sekar).

## 4. Kesimpulan
Skor BLEU 59.54 bersifat **bias**. Model terbukti "menghafal" lebih dari 60% frasa panjang yang diujikan. Evaluasi pada Test Set saat ini tidak mencerminkan kemampuan translasi pada kalimat yang benar-benar baru.

## 5. Rekomendasi
Diperlukan **Augmentasi Data** (EXP-003) untuk memperkaya variasi input dan pembuatan **Hard Test Set** (EXP-005) di masa mendatang.
