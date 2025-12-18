# Catatan Migrasi Proyek Bahasa Sekar (Arsip)

**Status:** Completed & Archived (18 Des 2025)
**Current Active Plan:** Lihat `PROJECT_PLAN.md`

Dokumen ini merekam proses pemindahan proyek dan setup awal di lingkungan baru. Seluruh langkah di bawah ini telah diselesaikan.

## Ringkasan Migrasi
1.  **Arsip Tesis Lama:** Berhasil dipindahkan ke `legacy_thesis/`.
2.  **Setup Python:** Virtual environment dan library GPU (`torch`, `transformers`, `nllb`) telah terpasang.
3.  **Baseline Training:** Model NLLB-200 berhasil dilatih (lihat `experiment_log_nllb.md`).

---
*(Bagian di bawah ini adalah panduan referensi jika perlu setup ulang)*

### Panduan Setup Ulang (Reference Only)

### 1. Setup Environment Python
```bash
# 1. Buat Virtual Environment
python3 -m venv .venv

# 2. Aktifkan (Linux/Mac)
source .venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install Dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets evaluate sacrebleu sentencepiece accelerate scikit-learn protobuf google-generativeai openai pandas
```

### 2. Verifikasi Instalasi
```bash
python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
```
