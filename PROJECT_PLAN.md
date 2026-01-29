# Rencana Proyek: Revitalisasi Bahasa Sekar

Status: **Active - Data Hardening Phase**
Last Updated: 29 Januari 2026

## 1. Fase Persiapan & Baseline (Selesai)
- [x] Pengumpulan Data & Cleaning.
- [x] Baseline MarianMT (BLEU ~28).
- [x] Migrasi ke NLLB-200 (BLEU ~60).
    - *Catatan:* Skor tinggi terindikasi bias karena overlap data.

## 2. Fase Validasi & Keamanan (Selesai)
- [x] **Audit Data Leakage (EXP-002)**
    - Menemukan overlap N-Gram >60% antara Train dan Test.
- [x] **Framework Eksperimen**
    - Struktur folder `experiments/` berbasis ID.
    - Kebijakan `READ-ONLY` untuk dataset inti.

## 3. Fase Augmentasi & Peningkatan Robustness (Current)
Fokus: Memperkaya variasi kalimat input (Indonesia) untuk mengurangi hafalan model.
- [x] **Setup DeepSeek API** untuk augmentasi data sintetik.
- [ ] **Data Augmentation (EXP-003)**
    - Paraphrasing data train menggunakan LLM.
    - Target: Melipatgandakan dataset menjadi >6000 pasang kalimat.
- [ ] **Retraining NLLB (EXP-004)**
    - Melatih ulang model dengan dataset campuran (Asli + Augmented).
    - Harapan: Model lebih tahan terhadap variasi struktur kalimat.

## 4. Fase Evaluasi Akhir & Deployment
- [ ] **Pembuatan "Hard Test Set"**
    - Kumpulan kalimat uji yang secara struktur *benar-benar baru* bagi model.
- [ ] **Human Evaluation**
    - Interface sederhana untuk penutur asli menilai keluwesan terjemahan.
- [ ] **Deployment**
    - Hugging Face Spaces & Hub.