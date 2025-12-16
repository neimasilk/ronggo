# Catatan Migrasi Proyek Bahasa Sekar

**Status Terakhir (16 Des 2025):**
1.  **Selesai:** Migrasi file Tesis lama ke `legacy_thesis/`.
2.  **Selesai:** Setup Environment Python (Virtualenv + GPU Support) berhasil.
3.  **Selesai:** Implementasi skrip training NLLB (`train_nllb.py`) sukses dijalankan.
4.  **Dokumentasi:** Detail teknis eksperimen NLLB dicatat di `07_NLLB_Experiment_Log.md`.

## Langkah Setup di Komputer Baru (Powerful Machine)

**CATATAN:** Setup ini telah dilakukan dan divalidasi pada sesi 16 Des 2025.

### 1. Setup Environment Python
Gunakan perintah ini jika perlu mengulang setup di mesin lain:

```bash
# 1. Buat Virtual Environment
python3 -m venv .venv

# 2. Aktifkan (Linux/Mac)
source .venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install Dependencies (GPU Support)
# Pastikan install PyTorch versi GPU (CUDA) jika mesin baru mendukung Nvidia CUDA!
# Cek https://pytorch.org/get-started/locally/ untuk perintah tepatnya, biasanya:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # Sesuaikan versi CUDA

# 5. Install Library NLP
pip install transformers datasets evaluate sacrebleu sentencepiece accelerate scikit-learn protobuf
```

### 2. Verifikasi Instalasi
Jalankan perintah ini untuk memastikan GPU terdeteksi:
```bash
python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
```

### 3. Lanjutkan Eksperimen (Baseline Model)
Kita siap membuat skrip training. Tugas selanjutnya adalah membuat file `train_nllb.py` dengan konfigurasi:
*   **Model:** `facebook/nllb-200-distilled-600M`
*   **Src Lang:** `ind_Latn` (Indonesian)
*   **Tgt Lang:** `eng_Latn` (Placeholder untuk Sekar, atau kita init lang code baru jika perlu, tapi untuk fine-tuning sementara bisa *hijack* lang code yang jarang dipakai).
*   **Hyperparams:** Batch size besar (karena mesin kuat), Learning rate rendah (2e-5).

*Happy Coding!*
