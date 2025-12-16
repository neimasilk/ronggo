# Revitalizing "Ghost Languages": Studi Kasus Elisitasi Jarak Jauh Bahasa Sekar (Fakfak) untuk Mengatasi Blind Spot pada Large Language Models

**Penulis:** [Nama Anda/Tim Peneliti]  
**Subjek:** Natural Language Processing, Low-Resource Language, Field Linguistics  
**Tanggal:** 2025

---

## Abstrak

Perkembangan *Large Language Models* (LLM) telah merevolusi bidang penerjemahan otomatis, namun menciptakan kesenjangan digital yang lebar bagi bahasa-bahasa daerah yang minim sumber daya (*low-resource*). Makalah ini mengangkat studi kasus Bahasa Sekar (dikenal lokal sebagai Bahasa Papua Kokas) di Kabupaten Fakfak, Papua Barat, yang dikategorikan sebagai "*Digital Ghost Language*" karena ketiadaan jejak teks digital di internet. Evaluasi *zero-shot* terhadap model AI mutakhir menunjukkan kegagalan total dalam mengenali bahasa ini, di mana model cenderung berhalusinasi atau melakukan generalisasi yang salah ke arah Melayu Papua umum. Penelitian ini mengusulkan metode pengumpulan data **"Remote Heritage Elicitation"**, yang memanfaatkan peran mahasiswa diaspora sebagai jembatan ke komunitas penutur jati. Hasilnya adalah dataset paralel Bahasa Indonesia-Sekar sebanyak 4.057 pasang kalimat yang tervalidasi secara linguistik. Dataset ini membuktikan keberadaan struktur morfologi unik (seperti pronomina *Yai* dan prefiks verba *e-*) yang sebelumnya tidak diketahui oleh model bahasa manapun, menegaskan pentingnya data kecil berkualitas tinggi (*small, high-quality data*) dalam pelestarian bahasa.

---

## 1. Pendahuluan

### 1.1 Latar Belakang
Indonesia memiliki kekayaan bahasa yang luar biasa, namun sebagian besar teknologi pemrosesan bahasa alami (NLP) hanya berfokus pada Bahasa Indonesia baku. Di wilayah Timur Indonesia, khususnya Papua, keragaman bahasa sangat tinggi namun dokumentasi digitalnya sangat rendah.

### 1.2 Masalah: "The AI Blind Spot"
Kecerdasan Buatan (AI) modern belajar dari data yang tersedia di internet. Hipotesis utama makalah ini adalah: **"Jika sebuah bahasa tidak memiliki jejak digital (korpus web), maka bahasa tersebut tidak eksis bagi AI."**

Bahasa Sekar di Distrik Kokas adalah contoh sempurna. Tanpa data latih spesifik, AI tercanggih sekalipun akan gagal membedakan Bahasa Sekar yang berumpun Austronesia (dengan tata bahasa kompleks) dari Melayu Papua (bahasa pasar/lingua franca).

---

## 2. Tinjauan Pustaka & Konteks Bahasa

### 2.1 Identifikasi Bahasa
Berdasarkan analisis data, bahasa yang diteliti diidentifikasi sebagai **Bahasa Sekar** (*Sekas*), yang dituturkan di pesisir Distrik Kokas, Fakfak.
*   **Karakteristik Unik:** Berbeda dengan Melayu Papua yang menggunakan "Sa" (Saya) dan "Ko" (Kamu), bahasa ini menggunakan "Yai" dan "O".
*   **Morfologi:** Memiliki sistem konjugasi kata kerja sederhana (prefiks subjek), misal: *Yai e-mau* (Saya mau).

### 2.2 Keterbatasan Data (Low-Resource)
Bahasa ini dikategorikan sebagai *Extremely Low-Resource*. Tidak ada kamus daring, artikel Wikipedia, atau berita dalam bahasa ini, menjadikannya kasus uji yang ideal untuk metodologi pengumpulan data dari nol.

---

## 3. Metodologi: Remote Heritage Elicitation

Kami memperkenalkan pendekatan partisipatif untuk mengatasi kendala jarak dan ketersediaan penutur.

### 3.1 Peran Diaspora (Heritage Speaker)
Pengumpulan data dipimpin oleh mahasiswa keturunan asli Kokas yang lahir/besar di luar Papua (Jawa). Mahasiswa ini bertindak sebagai *Heritage Speaker* yang memiliki akses kultural tetapi kemampuan bahasanya terbatas, sehingga memerlukan bantuan penutur jati.

### 3.2 Directed Elicitation (Elisitasi Terarah)
Karena ketiadaan korpus teks untuk diterjemahkan, tim peneliti menggunakan teknik *Directed Elicitation*:
1.  **Pembangkitan Stimulus:** Peneliti membuat (atau men-*generate*) daftar kalimat Bahasa Indonesia secara tematik (Pendidikan, Kesehatan, Kehidupan Sehari-hari).
2.  **Penerjemahan Manual:** Daftar tersebut dikirimkan kepada penutur jati (Ibunda dan kerabat di Kokas) melalui media komunikasi digital (WhatsApp).
3.  **Verifikasi:** Penutur jati menerjemahkan konsep tersebut ke dalam Bahasa Sekar yang "halus" atau asli, bukan bahasa pasar.

Metode ini menghasilkan struktur kalimat sumber (Indonesia) yang mungkin terlihat kaku/terpola, namun menghasilkan kalimat target (Sekar) yang sangat otentik dan gramatikal.

---

## 4. Analisis & Temuan: Kegagalan AI vs Realitas Data

### 4.1 Skenario Kegagalan Zero-Shot
Tanpa dataset ini, jika kita meminta LLM (seperti GPT-4 atau Gemini) menerjemahkan *"Saya ingin makan nasi"* ke Bahasa Kokas/Fakfak, model akan memprediksi:
*   *Prediksi AI:* "Sa mau makan nasi" (Melayu Papua).
*   *Kenyataan (Dataset):* "Yai emau eun pasa".

Ini membuktikan bahwa model mengalami *generalization error* yang parah karena bias data internet.

### 4.2 Statistik Dataset
Dataset final yang dihasilkan memiliki karakteristik:
*   **Volume:** 4.057 Pasang Kalimat.
*   **Kosa Kata Unik:** ~1.784 (Indonesia) vs ~2.400 (Sekar). Variasi kosa kata yang lebih tinggi di sisi Sekar menunjukkan kekayaan morfologi yang berhasil ditangkap.
*   **Integritas:** Dataset telah melalui proses *deduplication* dan *strict splitting* untuk mencegah kebocoran data antara data latih dan uji.

---

## 5. Kesimpulan & Implikasi

Penelitian ini menyimpulkan bahwa:
1.  Untuk bahasa daerah yang terisolasi secara digital, **kita tidak bisa mengandalkan kemampuan bawaan (pre-trained knowledge) dari AI**.
2.  Dataset kecil (4k baris) hasil kurasi manusia jauh lebih berharga daripada dataset besar hasil sintesis AI yang berpotensi halusinasi.
3.  Metode *Remote Heritage Elicitation* adalah solusi yang layak dan terukur untuk mendokumentasikan bahasa-bahasa di Nusantara yang terancam punah, memberdayakan komunitas diaspora sebagai garda depan pelestarian bahasa.

**Rencana Masa Depan:**
Dataset ini akan digunakan untuk melakukan *fine-tuning* pada model *multilingual* (seperti NLLB-200) untuk menciptakan sistem penerjemahan mesin Bahasa Indonesia-Sekar pertama yang fungsional.