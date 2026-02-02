# LOG Eksperimen EXP-005: Hard Test Set Creation

**Status:** Planned  
**Created:** 2 Februari 2026  
**Objective:** Membuat benchmark evaluasi yang lebih jujur dengan kalimat uji yang benar-benar baru secara struktural.

## 1. Latar Belakang
Model baseline (EXP-001) mencapai BLEU 59.54, namun audit EXP-002 menemukan overlap N-gram >60% antara train dan test. Hard Test Set dibuat untuk mengukur kemampuan generalisasi sebenarnya.

## 2. Metodologi

### 2.1 Kriteria Hard Test Set
Kalimat uji harus memenuhi:
- **Zero N-Gram Overlap:** Kombinasi kata yang tidak pernah muncul di training data
- **Struktur Baru:** Pola gramatikal yang berbeda dari data train
- **Vocabulary Langka:** Menggunakan kata-kata dari `dataset/rare_words_sekar.txt`

### 2.2 Proses Pembuatan
1. **Ekstraksi Kata Dasar:** Ambil kata-kata dasar Bahasa Sekar dari berbagai sumber
2. **Generate Kalimat Indonesia Baru:** Susun kalimat dengan struktur yang belum pernah ada
3. **Validasi Native Speaker:** Minta penutur asli translate ke Bahasa Sekar
4. **Verifikasi Overlap:** Pastikan tidak ada n-gram yang overlap dengan train set

## 3. Target Output
- **Ukuran:** 100-200 pasang kalimat
- **Format:** CSV (indonesian, papua_kokas)
- **Lokasi:** `dataset/test_hard.csv`

## 4. Hipotesis
- Model baseline kemungkinan akan perform jauh lebih buruk pada Hard Test Set
- Model EXP-004 (augmented data) diharapkan lebih robust
- Skor BLEU pada Hard Test Set akan menjadi metrik yang lebih representatif

## 5. Todo
- [ ] Analisis `rare_words_sekar.txt` untuk identifikasi vocabulary langka
- [ ] Buat script generator kalimat Indonesia dengan struktur baru
- [ ] Konsultasi dengan native speaker untuk terjemahan
- [ ] Verifikasi n-gram overlap dengan train set
- [ ] Finalisasi dataset dan dokumentasi

## 6. Dependencies
- Dataset: `dataset/rare_words_sekar.txt`
- Tools: Script n-gram analysis (reuse dari EXP-002)
