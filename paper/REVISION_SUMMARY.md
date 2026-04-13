# Ringkasan Revisi Paper JISEBI

**Tanggal Revisi:** 04 Februari 2026
**Deadline:** 16 Februari 2026

---

## Permintaan Reviewer dan Status

### 1. "Compare results using other methods besides transformers"
**Status: SELESAI**

Ditambahkan perbandingan dengan:
- **Word-based Dictionary Baseline** (BLEU 19.23)
- **LSTM Seq2Seq with Attention** (BLEU 30.74)
- **NLLB-200 Transformer** (BLEU 59.54)

Lokasi di paper:
- Methods → Model Configuration (deskripsi 3 metode)
- Results → Table 3: Comparison of Translation Methods
- Discussion → Comparative Analysis of Translation Approaches

### 2. "Explain what is so special about the language and how transformer mods help"
**Status: SELESAI**

Ditambahkan di Discussion section:
- **Linguistic Characteristics of Papua Kokas**
  - Unique pronominal system (yai/o vs saya/kamu)
  - Productive verbal morphology (e- prefix)
  - Word order variations

- **How Transformer Accommodates These Features**
  - Subword tokenization untuk morfologi
  - Multilingual transfer learning
  - Self-attention untuk long-range dependencies

---

## Perubahan Utama pada Paper

### Abstract
- Model: MarianMT → NLLB-200
- BLEU: 45-46 → 59.54
- Ditambahkan chrF++ (79.45) dan TER (27.70)
- Ditambahkan mention perbandingan metode
- Keywords: MarianMT → NLLB-200

### Methods
- Dataset: 2,908 → 4,057 sentence pairs
- Split: 90:10 → 80:10:10 (train/val/test)
- Model: MarianMT → NLLB-200 (600M params)
- Ditambahkan deskripsi Word Baseline dan LSTM Seq2Seq
- Evaluation Metrics: BLEU → BLEU, chrF++, TER

### Results
- Ditambahkan Table 3: Comparison of Translation Methods
- Updated training progress dengan NLLB-200
- Ditambahkan Table 5: Qualitative comparison

### Discussion
- Ditambahkan: Comparative Analysis of Translation Approaches
- Ditambahkan: Linguistic Characteristics of Papua Kokas
- Ditambahkan: How Transformer Accommodates (subword, transfer learning, self-attention)
- Updated: Comparison with Previous Studies
- Updated: Limitations

### Conclusion
- Updated dengan hasil perbandingan
- Emphasized chrF++ untuk morphological accuracy

### References
- Ditambahkan 3 referensi baru:
  - [24] NLLB Team - No Language Left Behind
  - [25] Popović - chrF metric
  - [26] Snover et al. - TER metric

---

## Checklist Compliance Status

| Item | Status | Notes |
|------|--------|-------|
| IMRaD format | ✅ | Introduction, Literature Review, Methods, Results, Discussion, Conclusion |
| Abstract 150-300 words | ✅ | ~280 words |
| Structured abstract | ✅ | Background, Objective, Methods, Results, Conclusion |
| 4-6 keywords | ✅ | 6 keywords |
| Research gap in Introduction | ✅ | Clearly stated |
| Methods cite sources | ✅ | NLLB-200 cited |
| Compare with other studies | ✅ | Comparison with Makassar, Madurese studies |
| Limitations section | ✅ | In Discussion |
| Author contributions | ✅ | CRediT taxonomy |
| References ≥20 | ✅ | 26 references |
| No bullets/numbering | ✅ | Converted to paragraphs |
| Acronyms defined | ✅ | NMT, BLEU, chrF++, TER, NLLB, LSTM defined |

---

## Files Modified/Created

### Eksperimen Baru (EXP-005)
```
experiments/EXP-005_Baseline_Comparison/
├── word_baseline.py          # Word dictionary baseline
├── lstm_seq2seq.py           # LSTM Seq2Seq with attention
├── evaluate_all.py           # Unified evaluation
├── LOG.md                    # Experiment log with results
├── lstm_model/best_model.pt  # Trained LSTM model
└── results/
    ├── comparison_table.csv
    ├── word_baseline_results.json
    ├── lstm_seq2seq_results.json
    └── word_dictionary.json
```

### Paper
```
paper/
├── draftpaper.md             # Updated paper draft
└── REVISION_SUMMARY.md       # This file
```

---

## Action Items Remaining

1. [ ] Convert draftpaper.md to JISEBI Word template
2. [ ] English proofreading/editing
3. [ ] Generate high-resolution figures (if needed)
4. [ ] Double-check all DOIs in references
5. [ ] Submit revised manuscript via OJS
6. [ ] Notify Editor

---

## Hasil Eksperimen Final

| Model | Architecture | BLEU | chrF++ | TER |
|-------|--------------|------|--------|-----|
| Word Baseline | Dictionary Lookup | 19.23 | 48.19 | 55.06 |
| LSTM Seq2Seq | Bi-LSTM + Attention | 30.74 | 58.63 | 47.01 |
| **NLLB-200** | **Transformer** | **59.54** | **79.45** | **27.70** |

**Key Finding:** Transformer (NLLB-200) menunjukkan peningkatan +94% dari LSTM dan +210% dari word baseline dalam BLEU score.
