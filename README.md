# Proyek Revitalisasi Bahasa Papua Kokas (Bahasa Sekar)

Repositori ini didedikasikan untuk pelestarian dan revitalisasi **Bahasa Sekar (Papua Kokas)** melalui teknologi kecerdasan buatan. Proyek ini berfokus pada pengembangan model *Machine Translation* (MT) untuk bahasa *low-resource* ini.

## Status Terkini: State-of-the-Art (NLLB-200)

Saat ini, kami telah berhasil mencapai performa terbaik menggunakan model **NLLB-200 (No Language Left Behind)** yang di-*fine-tune* pada dataset Bahasa Sekar.

### Metrik Performa
| Model | Epochs | Test BLEU | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| **NLLB-200** | 20 | **59.54** | **Active** | Diuji pada *Clean Test Set* (tanpa kebocoran data). |
| MarianMT (Baseline) | - | ~28.0 | Archived | - |

Hasil audit menunjukkan model sangat robust. Skor BLEU hanya turun 0.5 poin (dari 60.05 ke 59.54) setelah menghapus data test yang bocor/overlap dengan training.

### Limitasi Model (PENTING)
Meskipun skor metrik tinggi, model memiliki keterbatasan signifikan:
*   **Kalimat Panjang:** Model cenderung gagal (*repetition loop*) jika diberi input kalimat majemuk yang panjang (>15 kata).
*   **Domain Spesifik:** Sangat efektif untuk percakapan sehari-hari, namun akan banyak melakukan *copy-paste* kata untuk topik modern (teknologi, politik).

## Struktur Repositori

```
.
├── dataset/                # Dataset Paralel (Indonesian - Papua Kokas)
├── train_nllb.py           # Script training utama (NLLB-200)
├── inference_nllb.py       # Script untuk translasi/inferensi
├── inference_results_nllb.txt # Contoh hasil output model
├── experiment_log_nllb.md  # Log detail eksperimen NLLB
├── archive/                # Dokumentasi lama & log eksperimen terdahulu
└── nllb-sekar-finetuned/   # (Gitignored) Folder output model & checkpoint
```

## Cara Menggunakan

### 1. Instalasi Dependensi
Pastikan Anda menggunakan Python 3.10+ dan GPU (disarankan).
```bash
pip install transformers datasets evaluate sacrebleu sentencepiece accelerate torch
```

### 2. Training (Fine-tuning)
Untuk melatih ulang model dari awal:
```bash
python train_nllb.py
```
*Catatan: Proses ini memerlukan GPU (Tesla T4 atau lebih baik) dan memakan waktu sekitar 1 jam untuk 20 epoch.*

### 3. Inferensi (Menerjemahkan Kalimat)
Gunakan script inferensi untuk mencoba model yang telah dilatih:
```bash
python inference_nllb.py
```
Anda dapat mengedit `inference_nllb.py` untuk mengganti kalimat input.

## Roadmap & Eksperimen Selanjutnya
Lihat file [PROJECT_PLAN.md](PROJECT_PLAN.md) untuk roadmap lengkap dan [NEXT_EXPERIMENTS.md](NEXT_EXPERIMENTS.md) untuk ide teknis pengembangan selanjutnya.

## Kredit & Kontak
*   **Inisiator Data:** Ronggo Haikal
*   **Maintainer:** Neima Silk
*   **Lisensi:** MIT / CC-BY-SA (untuk dataset)