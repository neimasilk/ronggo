# Dataset Paralel Bahasa Indonesia - Papua Kokas

Dataset ini berisi pasangan kalimat Bahasa Indonesia dan terjemahannya dalam Bahasa Papua Kokas. Dataset ini telah dibersihkan dan distandarisasi dari berbagai sumber mentah untuk keperluan pengembangan *Machine Learning* dan *Natural Language Processing*.

## Struktur File

Direktori ini berisi file-file berikut:

- **master.csv**: Dataset lengkap yang berisi semua pasangan kalimat unik (4057 baris).
- **train.csv**: Data latih (80% dari total data) untuk melatih model.
- **val.csv**: Data validasi (10% dari total data) untuk evaluasi selama pelatihan.
- **test.csv**: Data uji (10% dari total data) untuk pengujian akhir model.

## Format Data

Semua file menggunakan format CSV (*Comma Separated Values*) dengan header sebagai berikut:

```csv
indonesian,papua_kokas
"kalimat dalam bahasa indonesia","kalimat dalam bahasa papua kokas"
...
```

## Statistik Dataset

- **Total Pasangan Unik:** 4.057
- **Split Ratio:** 80:10:10

## Catatan Penggunaan

Dataset ini cocok digunakan untuk tugas *Machine Translation* (Penerjemahan Mesin) seq2seq. Pastikan untuk melakukan tokenisasi yang sesuai sebelum memasukkan data ke dalam model neural network.

## Sumber Data

Dataset ini dikonsolidasikan dari berbagai file mentah dalam proyek `ronggo`, termasuk:
- `2908_data.csv`
- `Combined_Data.csv`
- `data_id_ko.csv`
- `data_2411.csv`
- `data_1855.csv`
