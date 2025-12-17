import pandas as pd

def normalize(text):
    # Lowercase dan strip whitespace untuk perbandingan yang adil
    return str(text).lower().strip().replace('.', '').replace(',', '')

print("--- MEMULAI AUDIT DATASET ---")

# Load Datasets
try:
    train_df = pd.read_csv("dataset/train.csv")
    test_df = pd.read_csv("dataset/test.csv")
except FileNotFoundError:
    print("Error: File dataset tidak ditemukan. Pastikan path benar.")
    exit()

print(f"Jumlah Data Training: {len(train_df)}")
print(f"Jumlah Data Testing:  {len(test_df)}")

# 1. Cek Kebocoran Langsung (Exact Match pada Source/Indonesian)
# Kita ubah kolom training ke set agar pencarian O(1)
train_src_set = set(train_df['indonesian'].apply(normalize))
test_src_normalized = test_df['indonesian'].apply(normalize)

# Cari mana yang overlap
leaks = test_df[test_src_normalized.isin(train_src_set)]
leak_count = len(leaks)
leak_percentage = (leak_count / len(test_df)) * 100

print("\n--- HASIL ANALISIS KEBOCORAN ---")
print(f"Total Kalimat Test yang BOCOR (ada di Training): {leak_count} dari {len(test_df)}")
print(f"Persentase Kebocoran: {leak_percentage:.2f}%")

if leak_count > 0:
    print("\n--- CONTOH KALIMAT BOCOR (5 Sampel) ---")
    print(leaks[['indonesian', 'papua_kokas']].head(5).to_string(index=False))

# 2. Cek Duplikasi Internal di Test Set
# Apakah test set itu sendiri isinya kalimat yang diulang-ulang?
test_dups = test_df['indonesian'].duplicated().sum()
print(f"\nDuplikasi Internal di Test Set: {test_dups} kalimat")

# 3. Kesimpulan Awal
print("\n--- KESIMPULAN AUDIT ---")
if leak_percentage > 10:
    print("STATUS: CRITICAL LEAKAGE. Skor BLEU tidak valid.")
elif leak_percentage > 0:
    print("STATUS: MINOR LEAKAGE. Skor BLEU mungkin sedikit bias.")
else:
    print("STATUS: CLEAN. Skor BLEU valid secara teknis (tapi perlu cek overfitting gaya bahasa).")
