# LOG Eksperimen EXP-004: Retraining with Augmented Data

**Status:** Planned / Ready to Run
**Source Data:** `../EXP-003_DeepSeek_Augmentation/augmented_train_v1.csv`

## Hipotesis
Dengan melatih ulang model menggunakan data yang telah diaugmentasi (parafrase Indonesia), model akan:
1.  Memiliki vocabulary Indonesia yang lebih luas.
2.  Tidak mudah *overfit* pada pola kalimat tertentu.
3.  Mungkin memiliki skor BLEU yang sedikit lebih rendah di "Dirty Test Set" lama, tapi lebih tinggi secara kualitatif.

## Cara Menjalankan
Pastikan proses augmentasi di EXP-003 sudah selesai 100% sebelum menjalankan ini.

```bash
python experiments/EXP-004_Retrain_Augmented/train_augmented.py
```
