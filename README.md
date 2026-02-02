# Proyek Revitalisasi Bahasa Papua Kokas (Bahasa Sekar)

Repositori ini didedikasikan untuk pelestarian dan revitalisasi **Bahasa Sekar (Papua Kokas)** melalui teknologi kecerdasan buatan. Proyek ini berfokus pada pengembangan model *Machine Translation* (MT) untuk bahasa *low-resource* ini.

## Status Terkini: Retraining dengan Data Augmented (NLLB-200)

Model baseline menggunakan **NLLB-200** mencapai skor BLEU **59.54** (EXP-001). Audit data (EXP-002) menemukan tingginya overlap frasa (>60%) antara train dan test yang memengaruhi skor. 

**Fase saat ini:** Data augmentation telah selesai (EXP-003), menghasilkan **6,478 pasang kalimat** (2x lipat). Selanjutnya: retraining model dengan dataset augmented (EXP-004) dan pembuatan Hard Test Set (EXP-005) untuk evaluasi yang lebih jujur.

### Metrik Performa
| Model | Test BLEU | Status | Catatan |
| :--- | :--- | :--- | :--- |
| **NLLB-200** | **59.54** | **Active** | *High Overlap Warning*. Sedang divalidasi ulang dengan dataset hasil augmentasi. |
| MarianMT | ~28.0 | Archived | Baseline awal. |

## Struktur Repositori

```
.
├── dataset/                # Dataset Paralel (Indonesian - Papua Kokas) [READ-ONLY]
├── experiments/            # Folder Eksperimen Terisolasi
│   ├── EXP-001.../         # Log Fine-tuning NLLB Baseline
│   ├── EXP-002.../         # Analisis N-Gram Overlap (Data Audit)
│   └── EXP-003.../         # Augmentasi Data dengan DeepSeek LLM
├── nllb-sekar-finetuned/   # (Gitignored) Folder output model & checkpoint
├── EXPERIMENT_REGISTRY.md  # Indeks seluruh eksperimen
├── PROJECT_PLAN.md         # Roadmap proyek
└── train_nllb.py           # Script training utama
```

## Cara Menggunakan

### 1. Instalasi Dependensi
Pastikan Python 3.10+ terinstall.
```bash
pip install transformers datasets evaluate sacrebleu sentencepiece accelerate torch openai python-dotenv
```

### 2. Setup Environment Variables
Proyek ini menggunakan API DeepSeek untuk augmentasi data. Buat file `.env` di root direktori:
```env
DEEPSEEK_API_KEY=sk-....
```

### 3. Training & Eksperimen
*   **Training NLLB:** `python train_nllb.py`
*   **Inferensi:** `python inference_nllb.py`
*   **Jalankan Eksperimen Baru:** Lihat `EXPERIMENT_REGISTRY.md` untuk panduan atau buat folder baru di `experiments/`.

## Roadmap
Lihat file [PROJECT_PLAN.md](PROJECT_PLAN.md) untuk detail rencana kerja, termasuk strategi augmentasi data sintetik yang sedang berjalan.

## Kredit & Kontak
*   **Inisiator Data:** Ronggo Haikal
*   **Maintainer:** Neima Silk
*   **Lisensi:** MIT / CC-BY-SA (untuk dataset)