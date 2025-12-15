# Review & Saran Perbaikan Paper

Berdasarkan analisis terhadap draft awal `Revitalizing_Papua_Kokas_Language.md`, berikut adalah poin-poin evaluasi dan saran perbaikan untuk meningkatkan kualitas paper agar memenuhi standar publikasi ilmiah (IEEE style):

## 1. Analisis Konten
-   **Kekuatan:** Alur cerita sudah jelas (Masalah -> Solusi -> Hasil). Skor BLEU yang tinggi (46.73) adalah poin penjualan utama.
-   **Kelemahan:**
    -   **Kurang Teknis pada Metodologi:** Bagian metodologi terlalu deskriptif. Perlu adanya formulasi matematis tentang bagaimana Transformer bekerja (mekanisme atensi) untuk menunjukkan kedalaman teknis.
    -   **Visualisasi Minim:** Tidak ada diagram alur sistem atau arsitektur model yang memudahkan pembaca memahami proses.
    -   **Analisis Hasil:** Skor BLEU 46 sangat tinggi untuk NMT. Perlu penjelasan kritis mengapa ini terjadi (apakah kalimatnya pendek/sederhana? apakah domainnya sangat tertutup?). Tanpa analisis ini, reviewer mungkin curiga terjadi *data leakage*.

## 2. Saran Perbaikan Spesifik
1.  **Format Matematika (LaTeX):** Tambahkan rumus fungsi objektif (Cross Entropy Loss) dan mekanisme Self-Attention. Ini standar wajib untuk paper NLP.
2.  **Visualisasi (Mermaid):**
    -   Tambahkan **Diagram Pipeline** (Data Prep -> Tokenizing -> Training -> Eval).
    -   Tambahkan **Diagram Arsitektur** sederhana yang menunjukkan Transfer Learning dari MarianMT.
3.  **Sitasi IEEE:** Ubah format referensi menjadi numerik `[1]`, `[2]` dan pastikan daftar pustaka mengikuti format IEEE.
4.  **Data Split:** Jelaskan secara eksplisit jumlah kalimat (angka pasti) untuk Train/Val/Test.
5.  **Diskusi:** Tambahkan paragraf yang membahas "Why MarianMT?" (efisiensi parameter vs training from scratch).

Saya akan segera merevisi paper tersebut dan menyimpannya sebagai **`Paper_Workspace/Revitalizing_Papua_Kokas_Language_v2.md`** dengan semua elemen di atas.
