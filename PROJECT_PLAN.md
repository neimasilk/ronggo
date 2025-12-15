# Rencana Strategis & Roadmap Pengembangan Proyek Bahasa Sekar (Kokas)

Dokumen ini merangkum strategi pengembangan proyek paska-Tugas Akhir untuk memastikan kontribusi mahasiswa (Ronggo Haikal) tetap dihargai sekaligus membuka ruang untuk inovasi riset lanjutan.

## Filosofi Utama: "Preservasi & Evolusi"
Tujuannya adalah membangun di atas pondasi yang sudah ada, bukan menggantinya. Dataset ini adalah aset langka ("emas"), dan metode pengumpulannya adalah nilai tambah unik.

---

## 1. Strategi Manajemen Repositori (Teknis)

Jangan membuat repositori baru. Pertahankan *history* Git untuk validitas data. Lakukan restrukturisasi:

*   **Arsip Warisan (`legacy_thesis/`)**:
    *   Buat folder baru bernama `legacy_thesis` atau `archive`.
    *   Pindahkan semua artefak asli mahasiswa ke sana: `laporan.pdf`, kode Django lama, skrip training MarianMT awal.
    *   Ini berfungsi sebagai referensi sejarah dan menghormati karya asli.
*   **Root untuk Pengembangan Baru**:
    *   Gunakan *root directory* untuk eksperimen baru yang lebih bersih (Python scripts modern, Docker, dll).
*   **Versioning**:
    *   Berikan *tag* pada commit terakhir sebelum perombakan (misal: `v1.0-student-thesis`) untuk "mengunci" keadaan saat lulus.

---

## 2. Peta Jalan Publikasi (Akademis)

Pecah output menjadi dua jalur berbeda untuk memaksimalkan dampak:

### Jalur A: "The Data Paper" (Fokus: Linguistik & Metodologi)
*   **Basis:** Draft `Paper_Draft_Ghost_Language.md`.
*   **Fokus:** Menyoroti fenomena "Ghost Language" dan metode *Remote Heritage Elicitation*.
*   **Kontribusi:** Dataset 4k baris yang valid dan metode pengumpulan data partisipatif.
*   **Posisi Penulis:** Mahasiswa (Ronggo) sebagai penulis utama/kedua (karena dia inisiator data), Anda sebagai *Corresponding Author*.
*   **Target:** Jurnal/Konferensi *Language Resources*, *Field Linguistics*, atau *Digital Humanities*.

### Jalur B: "The Modelling Paper" (Fokus: Teknikal & SOTA)
*   **Basis:** Eksperimen yang akan Anda lakukan (`Revitalizing_Papua_Kokas_Language_v2.md` yang dikembangkan).
*   **Fokus:** Mengalahkan *baseline* MarianMT pada kondisi *extremely low-resource*.
*   **Eksperimen Baru:**
    *   Fine-tuning **NLLB-200** atau **mBART**.
    *   Teknik Augmentasi Data (*Lexical Substitution*).
    *   Komparasi metrik evaluasi (BLEU vs CHRF).
*   **Posisi Penulis:** Tim peneliti baru/Anda sebagai penulis utama.
*   **Target:** Jurnal/Konferensi *Computer Science*, *AI*, atau *NLP*.

---

## 3. Hilirisasi & Dampak (Impact)

*   **Open Source Dataset (Hugging Face):**
    *   Upload `dataset/clean_dataset` ke Hugging Face Hub.
    *   Ini membuat dataset bisa diakses peneliti global, mengabadikan nama kontributor, dan memicu riset lanjutan dari pihak luar.
*   **Web App Modern:**
    *   Upgrade sistem lama ke stack yang lebih ringan (misal: FastAPI + Streamlit/React) agar mudah diakses via HP oleh masyarakat di Fakfak.

---

## 4. Langkah Taktis (To-Do List)

1.  [ ] **Housekeeping:** Jalankan `mkdir legacy_thesis` dan pindahkan file lama (`laporan.pdf`, dll).
2.  [ ] **Baseline:** Pastikan bisa mereproduksi hasil BLEU score dari data bersih menggunakan script evaluasi yang baru.
3.  **New Model:** Mulai eksperimen *fine-tuning* model **NLLB-200-Distilled** menggunakan dataset bersih.
4.  **Publish Data:** Buat akun Hugging Face dan upload dataset.

---
*Catatan dibuat pada: 15 Desember 2025*
