# LOG Eksperimen EXP-005: Baseline Comparison

**Status:** Ready to Run
**Tanggal:** 04 Februari 2026
**Tujuan:** Memenuhi permintaan reviewer JISEBI untuk perbandingan dengan metode selain Transformer

## 1. Latar Belakang

Reviewer JISEBI meminta:
> "authors need to compare their results using other methods besides transformers"

Eksperimen ini mengimplementasikan dua baseline untuk perbandingan:
1. **Word-based Dictionary** - Baseline statistik sederhana
2. **LSTM Seq2Seq** - Neural MT klasik (pre-Transformer era)

## 2. Metodologi

### 2A. Word-based Dictionary Baseline

**Prinsip:**
- Bangun dictionary word-to-word dari data training
- Untuk setiap kata Indonesia, cari terjemahan Papua Kokas yang paling sering muncul
- Translate kata per kata (OOV words di-copy as-is)

**Keterbatasan yang Diharapkan:**
- Tidak menangani word order
- Tidak memahami konteks
- Banyak OOV pada kata kompleks

### 2B. LSTM Seq2Seq dengan Attention

**Arsitektur:**
- Encoder: Bidirectional LSTM (2 layers)
- Decoder: LSTM dengan Bahdanau Attention
- Embedding dimension: 256
- Hidden dimension: 512
- Dropout: 0.3

**Hyperparameters:**
| Parameter | Nilai |
|-----------|-------|
| Batch Size | 32 |
| Learning Rate | 0.001 |
| Max Epochs | 100 |
| Early Stopping | 10 epochs |
| Min Word Freq | 2 |

## 3. Cara Menjalankan

### Prerequisites
```bash
pip install torch pandas evaluate tqdm transformers
```

### Run Individual Baselines
```bash
cd experiments/EXP-005_Baseline_Comparison

# Word baseline (cepat)
python word_baseline.py

# LSTM Seq2Seq (perlu training)
python lstm_seq2seq.py
```

### Run Unified Evaluation (semua model)
```bash
# Pastikan LSTM sudah ditraining dan NLLB model ada
python evaluate_all.py
```

## 4. Expected Results

| Model | Architecture | BLEU | chrF++ | TER |
|-------|--------------|------|--------|-----|
| Word Baseline | Dictionary Lookup | ~5-15 | ~25-35 | ~70-90 |
| LSTM Seq2Seq | Bi-LSTM + Attention | ~20-40 | ~45-60 | ~45-65 |
| **NLLB-200** | **Transformer** | **59.54** | **79.45** | **27.70** |

## 5. Output Files

```
results/
├── word_dictionary.json       # Word-to-word mapping
├── word_baseline_results.json # Word baseline metrics
├── lstm_seq2seq_results.json  # LSTM metrics + hyperparams
├── comparison_table.csv       # Final table for paper
└── all_results.json           # Combined detailed results
```

## 6. Signifikansi untuk Paper

Hasil eksperimen ini akan:
1. Menunjukkan bahwa **Transformer (NLLB-200) signifikan lebih baik** dari metode tradisional
2. Memvalidasi klaim bahwa arsitektur self-attention efektif untuk low-resource MT
3. Memenuhi requirement reviewer untuk perbandingan metode

## 7. Hasil Aktual

**Tanggal Eksperimen:** 04 Februari 2026

### Tabel Perbandingan Final

| Model | Architecture | BLEU | chrF++ | TER |
|-------|--------------|------|--------|-----|
| Word Baseline | Dictionary Lookup | **19.23** | 48.19 | 55.06 |
| LSTM Seq2Seq | Bi-LSTM + Attention | **30.74** | 58.63 | 47.01 |
| **NLLB-200** | **Transformer** | **59.54** | **79.45** | **27.70** |

### Analisis Hasil

1. **Word Baseline (BLEU 19.23)**
   - Lebih tinggi dari prediksi awal (~5-15), menunjukkan dataset punya pola sederhana
   - Banyak error karena word order tidak ditangani
   - Berguna sebagai lower-bound

2. **LSTM Seq2Seq (BLEU 30.74)**
   - Peningkatan +60% dari word baseline
   - Early stopping di epoch 15 (overfitting mulai terdeteksi)
   - Model ~18M parameters
   - Masih kalah signifikan dari Transformer

3. **NLLB-200 Transformer (BLEU 59.54)**
   - **Peningkatan +94% dari LSTM** dan +210% dari word baseline
   - chrF++ sangat tinggi (79.45) menunjukkan penguasaan morfologi
   - TER rendah (27.70) berarti sedikit post-editing diperlukan

### Kesimpulan

Hasil eksperimen **mendukung klaim paper** bahwa:
- Transformer (NLLB-200) **signifikan lebih baik** dari metode tradisional
- Self-attention mechanism efektif untuk low-resource NMT
- Transfer learning dari model multilingual sangat bermanfaat

---

## Catatan

- LSTM mungkin memerlukan GPU untuk training yang cepat
- Word baseline bisa langsung dijalankan (tidak perlu training)
- Pastikan `nllb-sekar-finetuned/final_model` tersedia untuk evaluasi NLLB
