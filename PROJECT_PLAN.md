# Rencana Proyek: Revitalisasi Bahasa Sekar

Status: **Active**
Last Updated: 18 Desember 2025

## 1. Fase Persiapan Data (Selesai)
- [x] Pengumpulan Data (Remote Heritage Elicitation)
- [x] Pembersihan Data (Cleaning & Formatting)
- [x] Pembagian Dataset (Train/Val/Test)
- [x] Konversi ke format CSV yang kompatibel dengan Hugging Face Datasets.

## 2. Fase Baseline Model (Selesai)
- [x] Implementasi MarianMT (Helsinki-NLP)
- [x] Evaluasi Baseline (BLEU score awal ~28)
- [x] Analisis Error Baseline.

## 3. Fase Modernisasi Model (Selesai)
- [x] **Migrasi ke NLLB-200 (No Language Left Behind)**
    - Menggunakan model `facebook/nllb-200-distilled-600M`.
    - Strategi: Language Transfer (menggunakan placeholder `eng_Latn` -> `ind_Latn`).
- [x] **Fine-tuning Full (20 Epochs)**
    - Learning Rate: 2e-5, Batch Size: 16, fp16.
- [x] **Pencapaian:**
    - Test BLEU: **60.05** (High score, potential overfitting on simple sentences).
    - chrF++: **79.45** (Strong morphological capture).
- [x] **Identifikasi Masalah (Limitation):**
    - Model gagal pada kalimat majemuk/kompleks (terjadi *repetition loop*).
    - Dataset terlalu kecil (~3200 train) untuk generalisasi struktur kalimat yang rumit.

## 4. Fase Data Augmentation (Active - Current Focus)
Fokus: Mengatasi kekurangan data dan isu kalimat kompleks menggunakan **LLM dengan Strict Constraints**.
- [x] **Setup Pipeline LLM (Selesai)**
    - [x] Buat script ekstraktor kamus (`dataset/scripts/build_dictionary.py`).
    - [x] Buat script generator (`dataset/scripts/generate_synthetic_llm.py`) dengan integrasi Gemini/DeepSeek.
    - [x] Implementasi **3 Golden Rules**: Complexity, NER Preservation, & Dictionary Fallback (Code Mixing).
    - [x] Buat script penggabung aman (`dataset/scripts/combine_datasets.py`) agar data asli tidak tertimpa.
- [ ] **Generasi Data Sintetis (Next Step)**
    - [ ] Run Generator Batch 1 (Target: 50-100 kalimat untuk validasi manual).
    - [ ] Run Generator Full Batch (Target: +1000-2000 kalimat).
    - [ ] Gabungkan dataset (Original + Synthetic).
- [ ] **Training dengan Data Augmentasi**
    - [ ] Fine-tune ulang NLLB-200 dengan `train_augmented.csv`.
    - [ ] Evaluasi apakah masalah *repetition loop* teratasi.

## 5. Fase Evaluasi & Deployment (Pending)
- [ ] Analisis Kualitatif Mendalam (Human Evaluation oleh penutur asli).
- [ ] Deployment ke Web Interface (Hugging Face Spaces).
- [ ] Publikasi Model ke Hugging Face Hub.

## 6. Eksperimen Lanjutan (Backlog)
Lihat detail di `NEXT_EXPERIMENTS.md`.