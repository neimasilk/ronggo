# CONTEXT & STATE RECOVERY FOR GEMINI AGENT
**Last Updated:** 17 Desember 2025
**Status:** Private Local File (Gitignored)

## 1. System Recovery (Colab Reset)
Jika environment Google Colab baru saja di-reset, jalankan perintah ini segera untuk memulihkan akses Git:
```bash
./restore_git.sh
```
*Script ini berisi token GitHub (ghp_...) yang tidak boleh dipublikasikan.*

## 2. Git Branching Status & Strategy
Penting: Branch eksperimen saat ini **hanya tersimpan lokal** di Google Drive. Belum di-push ke GitHub.

| Branch Name | Status | Deskripsi |
| :--- | :--- | :--- |
| **`main`** | Remote & Local | **Stable.** Berisi model NLLB Baseline (BLEU 59.54). Sinkron dengan GitHub. |
| **`exp/synthetic-data`** | **Local Only** | **Active Experiment.** Branch untuk pengembangan data sintetis (Back-Translation). **JANGAN HAPUS FOLDER .git**. |

*Catatan: Jika ingin membackup branch eksperimen ini ke GitHub, jalankan `git push -u origin exp/synthetic-data` nanti.*

## 3. Active Experiment: Synthetic Data
Kita sedang dalam tahap persiapan eksperimen data sintetis.
*   **Active Directory:** `/content/drive/MyDrive/Colab Notebooks (1)/ronggo/ronggo/`
*   **Folder Kerja:** `experiments/02_synthetic_data/`
*   **Folder Data Target:** `dataset/synthetic/`
*   **Tujuan:** Mengatasi masalah *repetition loop* pada kalimat panjang dengan Back-Translation.

## 4. Next Action Items
Tugas yang harus dikerjakan saat sesi berikutnya dimulai:
1.  **Generate Data:** Buat script `experiments/02_synthetic_data/generate_synthetic.py`.
    *   Fungsi: Load model NLLB (Sekar->Indo), ambil dataset monolingual Indo, translate ke Sekar.
2.  **Training:** Jalankan `train_augmented.py` dengan data gabungan.

## 5. Important Notes
*   **Data Leakage:** Isu kebocoran data (12.4%) sudah diselesaikan di branch `main`. Jangan ulangi kesalahan ini saat membuat split data baru.
*   **Limitasi Model:** Model saat ini *overfit* pada kalimat pendek. Data sintetis diharapkan memperbaiki ini.