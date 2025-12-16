# Laporan Eksplorasi Data: Bahasa Sekar (Papua Kokas)
**Tanggal:** 16 Desember 2025  
**Penulis:** Gemini Agent  
**Tujuan:** Memahami karakteristik linguistik, statistik, dan integritas dataset sebelum pemodelan mesin.

## 1. Ringkasan Statistik
Analisis dilakukan pada file `dataset/master.csv` (Total 4.056 pasangan kalimat).

| Metrik | Bahasa Indonesia (Sumber) | Bahasa Sekar (Target) |
| :--- | :--- | :--- |
| **Rata-rata Panjang Kalimat** | 7.68 kata | 8.35 kata |
| **Ukuran Kosakata (Vocab)** | 1.938 kata unik | 2.639 kata unik |
| **Type-Token Ratio (TTR)** | 0.0622 | 0.0779 |

**Insight:**
*   Bahasa Sekar memiliki kalimat yang sedikit lebih panjang (+0.67 kata/kalimat) dibanding Bahasa Indonesia.
*   Kosakata Bahasa Sekar jauh lebih kaya (+36%) dibanding sumbernya. Hal ini menarik karena sumbernya adalah kalimat templat. Hipotesis: Adanya variasi morfologi (prefix/suffix) yang dihitung sebagai kata unik berbeda oleh tokenizer sederhana, atau adanya variasi sinonim dalam penerjemahan natural.

## 2. Analisis Frekuensi Kata (Top Words)
Identifikasi kata kunci untuk memvalidasi bahasa.

**Bahasa Sekar (Kokas) Top 5:**
1.  **o** (1.744) -> Teridentifikasi sebagai "Kamu" (bukan "Ko" seperti Melayu Papua umum).
2.  **adi** (1.624) -> Kata fungsi frekuensi tinggi (kemungkinan preposisi atau konjungsi).
3.  **akape** (1.360) -> Teridentifikasi sebagai "Bagaimana" atau "Apa".
4.  **ami** (1.247) -> Kemungkinan preposisi "di" atau "dalam".
5.  **kusafa** (858) -> Kata tanya.

**Fenomena Code-Mixing:**
Ditemukan kata Bahasa Indonesia dalam daftar frekuensi tinggi Bahasa Sekar:
*   *yang* (570)
*   *bisa* (543)
*   *cara* (503)
*   *indonesia* (328)

**Kesimpulan:** Bahasa ini mengalami pencampuran kode (*code-mixing*) yang signifikan atau peminjaman kata (*loan words*) untuk konsep-konsep modern atau abstrak.

## 3. Analisis Struktur (N-Grams)
Mendeteksi pola kalimat berulang (templat).

**Top Trigrams (3 Kata Berurutan):**
1.  *o pendapat akape* (352) -> "Bagaimana pendapat kamu"
2.  *kwai kusafa yang* (294) -> "Apa hal yang..." (dugaan)
3.  *akape ita cara* (234) -> "Bagaimana cara kita..."

Data menunjukkan struktur yang sangat terpola (*highly structured/repetitive*). Ini adalah pedang bermata dua:
*   (+) Mudah bagi model untuk mempelajari pola dasar gramatika.
*   (-) Model mungkin *overfit* pada templat ini dan gagal jika diberi kalimat di luar distribusi templat.

## 4. Verifikasi Kebocoran Data (Data Leakage)
Pengecekan himpunan irisan (*intersection*) antara kalimat sumber di Data Latih (`train.csv`) dan Data Uji (`test.csv`).

*   Jumlah Unik Train: 3.192
*   Jumlah Unik Test: 399
*   **Overlap (Kebocoran): 0**

**Status:** **AMAN.** Metode *Strict Splitting* berhasil. Evaluasi performa model di masa depan akan valid dan tidak bias.

## 5. Rekomendasi Tindak Lanjut
1.  **Preprocessing:** Perlu normalisasi kata serapan jika tujuannya adalah purifikasi bahasa, namun untuk tujuan pelestarian kondisi riil, biarkan apa adanya.
2.  **Model:** Gunakan model *multilingual pre-trained* (NLLB-200) karena kosa kata yang terbatas namun struktur kalimat yang kompleks.
3.  **Augmentasi:** Karena pola sangat repetitif (misal: "Bagaimana cara..."), kita bisa melakukan *Lexical Substitution* pada objek kalimat untuk memperkaya data latih secara sintetik.
