# Dataset Paralel Bahasa Indonesia - Bahasa Sekar (Papua Kokas)

Dataset ini berisi pasangan kalimat Bahasa Indonesia dan terjemahannya dalam **Bahasa Sekar**, sebuah bahasa daerah yang dituturkan di wilayah Distrik Kokas, Kabupaten Fakfak, Papua Barat.

## Identifikasi Bahasa

Meskipun dalam laporan penelitian asli disebut secara umum sebagai "Bahasa Papua Kokas", analisis linguistik terhadap data ini menunjukkan karakteristik kuat dari **Bahasa Sekar** (bagian dari rumpun bahasa *North Bomberai* dalam keluarga Austronesia).

**Bukti Identifikasi:**
*   **Kata Ganti (Pronouns):** Penggunaan kata **"Yai"** (Saya) dan **"O"** (Kamu). Ini berbeda dengan Melayu Papua umum ("Sa", "Ko") atau Bahasa Iha ("On").
*   **Morfologi:** Adanya penggunaan awalan (prefix) pada kata kerja yang mengikuti subjek (contoh: *"Yai **e**-mau **e**-ti"*), yang merupakan ciri khas tata bahasa Austronesia (Sekar).
*   **Lokasi:** Data dikumpulkan melalui wawancara dengan keluarga penutur asli di Distrik Kokas (khususnya wilayah penutur Bahasa Sekar).

## Latar Belakang & Metodologi Pengumpulan Data

Dataset ini memiliki nilai unik karena dikumpulkan melalui metode **Elisitasi Jarak Jauh dengan Komunitas Penutur Jati (Remote Elicitation with Heritage Community)**.

*   **Konteks Peneliti:** Pengumpul data adalah mahasiswa keturunan Papua (Diaspora) yang lahir di Jawa dan tidak lagi fasih berbahasa daerah, namun memiliki akses langsung ke penutur asli (Ibunda dan Kerabat).
*   **Proses Elisitasi:** Kalimat sumber Bahasa Indonesia disusun secara tematik (misal: topik sekolah, kesehatan, hobi) sebagai stimulus/pancingan oleh tim peneliti.
*   **Validasi Penutur Asli:** Terjemahan dilakukan secara manual oleh **Ibunda dan Kerabat peneliti** yang merupakan penutur jati (*native speakers*) generasi tua dari Distrik Kokas melalui korespondensi digital (WhatsApp). 
*   **Signifikansi:** Metode ini memastikan bahwa meskipun kalimat sumber Bahasa Indonesianya terpola (*template-based* hasil *generation* ide), terjemahan sasarannya adalah murni dan valid secara linguistik (Bahasa Sekar asli/halus), bukan sekadar Melayu Papua pasar.

## Struktur File

Dataset telah dibersihkan, dideduplikasi, dan dibagi dengan metode *strict splitting* (berbasis kalimat unik Indonesia) untuk mencegah kebocoran data (*data leakage*).

- **master.csv**: Dataset lengkap yang berisi seluruh pasangan kalimat unik (4.057 baris).
- **train.csv**: Data latih (3.239 baris) untuk melatih model.
- **val.csv**: Data validasi (407 baris) untuk evaluasi selama pelatihan.
- **test.csv**: Data uji (410 baris) untuk pengujian akhir model.

## Format Data

Semua file menggunakan format CSV (*Comma Separated Values*) dengan header:

```csv
indonesian,papua_kokas
"saya ingin makan nasi","yai emau eun pasa"
"bagaimana kabarmu","akape o habar"
```

## Statistik Dataset

- **Total Pasangan Unik:** 4.057
- **Rata-rata Panjang Kalimat:** ~7-8 kata.
- **Kosa Kata Unik (Vocabulary):**
    - Bahasa Indonesia: ~1.784 kata
    - Bahasa Sekar (Kokas): ~2.400 kata

## Catatan Penggunaan (Low Resource Language)

Bahasa Sekar adalah *Low Resource Language* (Bahasa dengan Sumber Daya Rendah).
1.  **Pola Berulang:** Sebagian data memiliki pola kalimat repetitif. Ini sangat berguna untuk mempelajari struktur dasar bahasa (SPOK) bagi mesin.
2.  **Rekomendasi Model:** Disarankan menggunakan pendekatan *Transfer Learning* (seperti fine-tuning NLLB-200 atau mBART) daripada melatih model dari nol (*from scratch*).
3.  **Augmentasi:** Dataset ini sangat ideal dijadikan basis untuk *Rule-Based Augmentation* (misal: substitusi kata benda/objek) untuk memperbanyak jumlah data latih.

## Manajemen Data (Gold vs Silver)

Untuk menjaga integritas data penelitian, kami menerapkan pemisahan ketat antara data asli (validasi manusia) dan data hasil augmentasi komputer.

### 1. Data Emas (Gold Standard)
File `train.csv`, `val.csv`, dan `test.csv` di folder ini adalah **DATA MURNI**.
*   **Status:** Read-Only (Jangan pernah diedit manual kecuali ada perbaikan error validasi).
*   **Sumber:** Validasi Penutur Asli.
*   **Fungsi:** Menjadi acuan kebenaran (Ground Truth).

### 2. Data Perak (Silver / Synthetic)
Data hasil generasi AI (LLM) disimpan di folder `dataset/synthetic/`.
*   **Status:** Eksperimental.
*   **Sumber:** Google Gemini / DeepSeek (dengan pengawasan aturan ketat).
*   **Fungsi:** Menambah variasi struktur kalimat untuk training.

### 3. Data Latih Gabungan (Augmented)
Sebelum melakukan training model, data Emas dan Perak digabungkan.
*   **Script:** Jalankan `python dataset/scripts/combine_datasets.py`.
*   **Output:** Akan menghasilkan file `dataset/train_augmented.csv`.
*   **Git Policy:** File ini **DIABAIKAN** oleh Git (`.gitignore`) karena bersifat sementara dan redundan. Jangan pernah meng-commit file ini.

---

## Sumber Data

Dataset ini dikonsolidasikan dan direstorasi dari proyek penelitian mahasiswa (Ronggo Haikal, 2024) melalui studi kasus dan wawancara mendalam dengan narasumber keluarga di Daerah Kokas.
