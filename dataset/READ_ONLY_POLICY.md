# KEBIJAKAN KEAMANAN DATASET (CORE)

⚠️ **PERINGATAN KERAS** ⚠️

Folder ini berisi **Dataset Inti (Golden Source)** yang dikumpulkan secara manual.

1.  **READ-ONLY**: File `master.csv`, `train.csv`, `val.csv`, dan `test.csv` **DILARANG** dimodifikasi, ditimpa, atau dihapus oleh skrip otomatis apapun.
2.  **NON-DESTRUCTIVE**: Jika Anda ingin melakukan pembersihan, normalisasi, atau augmentasi, simpan hasil outputnya sebagai **file baru** (misal: `train_cleaned_v2.csv` atau di folder `dataset/derivatives/`), JANGAN menimpa file asli.
3.  **BACKUP**: Pastikan cadangan data ini tersedia di lokasi terpisah.

File ini berfungsi sebagai pengingat prosedural untuk menjaga integritas data riset.
