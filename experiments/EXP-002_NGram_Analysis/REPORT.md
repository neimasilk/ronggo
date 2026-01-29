# Laporan Eksperimen EXP-002: Analisis Overlap N-Gram

**Tanggal:** 29 Januari 2026
**Tujuan:** Memvalidasi independensi dataset Test terhadap Train. Skor BLEU yang tinggi mencurigakan jika overlap N-Gram terlalu tinggi.

## 1. Analisis Bahasa Indonesia (Source)
Seberapa mirip kalimat input di Test dengan Train?

| N-Gram | Total di Test | Overlap (Hafalan) | % Overlap | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1-gram | 3061 | 2972 | **97.09%** | ⚠️ BAHAYA |
| 2-gram | 2651 | 2184 | **82.38%** | ⚠️ BAHAYA |
| 3-gram | 2241 | 1549 | **69.12%** | ⚠️ WASPADA |
| 4-gram | 1831 | 1120 | **61.17%** | ⚠️ WASPADA |

## 2. Analisis Bahasa Sekar (Target)
Seberapa mirip kalimat output yang diharapkan di Test dengan Train?

| N-Gram | Total di Test | Overlap (Hafalan) | % Overlap | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1-gram | 3309 | 3177 | **96.01%** | ⚠️ BAHAYA |
| 2-gram | 2899 | 2254 | **77.75%** | ⚠️ BAHAYA |
| 3-gram | 2489 | 1596 | **64.12%** | ⚠️ WASPADA |
| 4-gram | 2079 | 1179 | **56.71%** | ⚠️ WASPADA |

## 3. Kesimpulan
Jika overlap pada 3-gram dan 4-gram melebihi 50%, maka sebagian besar frasa yang diuji sebenarnya sudah pernah dilihat model saat training. Ini menjelaskan kenapa BLEU score tinggi.
