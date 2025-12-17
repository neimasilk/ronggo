# Rencana Proyek: Revitalisasi Bahasa Sekar

Status: **Active**
Last Updated: 17 Desember 2025

## 1. Fase Persiapan Data (Selesai)
- [x] Pengumpulan Data (Remote Heritage Elicitation)
- [x] Pembersihan Data (Cleaning & Formatting)
- [x] Pembagian Dataset (Train/Val/Test)
- [x] Konversi ke format CSV yang kompatibel dengan Hugging Face Datasets.

## 2. Fase Baseline Model (Selesai)
- [x] Implementasi MarianMT (Helsinki-NLP)
- [x] Evaluasi Baseline (BLEU score awal ~28)
- [x] Analisis Error Baseline.

## 3. Fase Modernisasi Model (Selesai - Current State)
- [x] **Migrasi ke NLLB-200 (No Language Left Behind)**
    - Menggunakan model `facebook/nllb-200-distilled-600M`.
    - Strategi: Language Transfer (menggunakan placeholder `eng_Latn` -> `ind_Latn`).
- [x] **Fine-tuning Full (20 Epochs)**
    - Learning Rate: 2e-5
    - Batch Size: 16
    - Mixed Precision (fp16)
- [x] **Pencapaian:**
    - Test BLEU: **60.05** (Peningkatan signifikan >100% dari baseline).
    - Model stabil dan konvergen.

## 4. Fase Evaluasi & Deployment (In Progress)
- [x] Script Inferensi (`inference_nllb.py`)
- [ ] Analisis Kualitatif Mendalam (Human Evaluation oleh penutur asli).
- [ ] Deployment ke Web Interface (Hugging Face Spaces).
- [ ] Publikasi Model ke Hugging Face Hub.

## 5. Eksperimen Lanjutan (Planned)
Lihat detail di `NEXT_EXPERIMENTS.md`.