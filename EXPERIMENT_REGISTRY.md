# Registry Eksperimen: Revitalisasi Bahasa Sekar

File ini mencatat seluruh riwayat eksperimen, baik yang berhasil, gagal, maupun yang masih berjalan. Tujuannya adalah menjaga kontinuitas pengetahuan.

## Status Legend
*   **Planned**: Direncanakan, belum dimulai.
*   **In Progress**: Sedang berjalan.
*   **Completed**: Selesai dengan hasil konklusif.
*   **Failed**: Gagal karena error teknis atau hasil tidak sesuai hipotesis (tetap dicatat untuk pembelajaran).
*   **Archived**: Eksperimen lama yang sudah tidak relevan tapi disimpan untuk sejarah.

## Daftar Eksperimen

| ID | Judul | Tanggal Mulai | Status | Hasil Utama / Catatan |
| :--- | :--- | :--- | :--- | :--- |
| **EXP-001** | [NLLB-200 Fine-tuning Baseline](experiments/EXP-001_NLLB_Baseline/LOG.md) | 16-12-2025 | **Completed** | BLEU 59.54. Model sangat stabil tapi repetitif pada kalimat panjang. |
| **EXP-002** | [Analisis Overlap N-Gram (Data Validity)](experiments/EXP-002_NGram_Analysis/LOG.md) | 29-01-2026 | **Completed** | Overlap tinggi (>60% di 4-gram). Perlu augmentasi. |
| **EXP-003** | [Data Augmentation with DeepSeek LLM](experiments/EXP-003_DeepSeek_Augmentation/LOG.md) | 29-01-2026 | **Completed** | 100% data (6478 rows) berhasil diaugmentasi. |
| **EXP-004** | [Retraining with Augmented Data](experiments/EXP-004_Retrain_Augmented/LOG.md) | 29-01-2026 | **In Progress** | Melatih ulang NLLB-200 dengan dataset augmented. |
