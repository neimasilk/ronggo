# Eksperimen 02: Synthetic Data Augmentation (Back-Translation)

**Status:** Planned
**Branch:** `exp/synthetic-data`

## Tujuan
Meningkatkan performa model NLLB-200 (terutama mengatasi *repetition loop* pada kalimat panjang) dengan memperbanyak data latih menggunakan teknik Back-Translation.

## Rencana Kerja
1.  **Reverse Training:** Latih model Sekar -> Indonesia.
2.  **Sourcing:** Cari dataset monolingual Bahasa Indonesia (Wikipedia/Buku Cerita) ~5.000 kalimat.
3.  **Generation:** Terjemahkan dataset monolingual tersebut ke Sekar menggunakan Reverse Model.
4.  **Augmentation:** Gabungkan Data Asli + Data Sintetis.
5.  **Final Training:** Latih model Indonesia -> Sekar dengan data gabungan.

## File Struktur
*   `train_augmented.py`: Script training utama (modifikasi dari `train_nllb.py`).
*   `generate_synthetic.py`: (Belum dibuat) Script untuk back-translation.
