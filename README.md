# Proyek Revitalisasi Bahasa Papua Kokas (Bahasa Sekar)

Repositori ini berisi aset digital, dataset, laporan penelitian, dan draft publikasi ilmiah yang bertujuan untuk mendokumentasikan dan merevitalisasi Bahasa Sekar (dikenal secara lokal sebagai Bahasa Papua Kokas) di Kabupaten Fakfak, Papua Barat. Bahasa ini dikategorikan sebagai *low-resource language* dengan jejak digital yang sangat minim.

## Daftar Isi Dokumen

Berikut adalah panduan untuk memahami dokumen-dokumen yang ada dalam repositori ini:

### 1. Dataset (`/dataset`)
Ini adalah komponen paling berharga dari repositori ini. Folder ini berisi korpus paralel Bahasa Indonesia - Bahasa Sekar yang telah dibersihkan dan distandarisasi.
*   **Isi:** Dataset pelatihan, validasi, dan pengujian.
*   **Metodologi:** Data dikumpulkan melalui metode *Remote Heritage Elicitation*, di mana kalimat stimulus Bahasa Indonesia diberikan kepada penutur jati (generasi tua di Kokas) untuk diterjemahkan secara manual.
*   **Detail:** Lihat `dataset/README.md` untuk informasi teknis lengkap.

### 2. Laporan Tugas Akhir (`laporan.pdf`)
*   **Deskripsi:** Dokumen asli skripsi/tugas akhir mahasiswa (Ronggo Haikal, 2024).
*   **Konteks:** Mahasiswa ini adalah inisiator pengumpulan data. Karena mahasiswa sudah lulus dan sulit dihubungi, dokumen ini menjadi referensi utama mengenai asal-usul data awal.
*   **Isi:** Menjelaskan proses wawancara, implementasi awal model MarianMT, dan hasil evaluasi BLEU skor pada tahap awal penelitian.

### 3. Paper Ilmiah (Draft)

Terdapat dua draft publikasi yang dikembangkan dari hasil penelitian ini dengan fokus yang berbeda:

*   **`Revitalizing_Papua_Kokas_Language_v2.md`**
    *   **Fokus:** Implementasi Teknis & Eksperimen.
    *   **Isi:** Membahas arsitektur *Transfer Learning* menggunakan MarianMT, konfigurasi *hyperparameter*, dan hasil eksperimen kuantitatif. Ini adalah versi akademis formal dari Laporan TA yang disiapkan untuk konferensi atau jurnal teknik informatika/komputer.

*   **`Paper_Draft_Ghost_Language.md`**
    *   **Fokus:** Linguistik Komputasional & Metodologi Data.
    *   **Isi:** Menyoroti fenomena "Ghost Language" (bahasa tanpa jejak digital) dan kegagalan model AI besar (*Large Language Models*) dalam mengenali bahasa ini secara *zero-shot*. Paper ini mengajukan metode *Remote Heritage Elicitation* sebagai solusi novel untuk mengatasi *blind spot* pada AI.

### 4. Dokumen Lainnya
*   **`01_Abstract_Intro.md` s.d. `05_Conclusion.md`**: Pecahan bab dari draft paper awal (v1).
*   **`Review_Report.md`**: Catatan review internal terhadap kualitas dataset dan metodologi.

## Ringkasan Proyek

Proyek ini adalah jembatan antara teknologi AI modern dengan pelestarian budaya tradisional. Melalui kolaborasi antara akademisi, mahasiswa diaspora, dan komunitas penutur jati, kami berhasil membangun dataset digital pertama yang valid untuk Bahasa Sekar, membuka jalan bagi pengembangan teknologi bahasa untuk komunitas yang terpinggirkan secara digital.
