import csv
import os
import statistics

dataset_dir = 'dataset/clean_dataset'
files = {'Train': 'train.csv', 'Val': 'val.csv', 'Test': 'test.csv'}

def simple_tokenize(text):
    # Tokenisasi sederhana: split by space
    # Remove common punctuation agar tidak menempel di kata
    for char in '.,?!- ";:()':
        text = text.replace(char, ' ') # ganti dengan spasi
    return [w for w in text.split() if w] # Hapus string kosong

def analyze_split(name, file_path):
    indo_sentences = []
    kokas_sentences = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            indo_sentences.append(row['indonesian'])
            kokas_sentences.append(row['papua_kokas'])
            
    num_samples = len(indo_sentences)
    
    # Statistik Panjang Kalimat (Jumlah Kata)
    indo_lens = [len(simple_tokenize(s)) for s in indo_sentences]
    kokas_lens = [len(simple_tokenize(s)) for s in kokas_sentences]
    
    # Vocabulary
    indo_vocab = set()
    kokas_vocab = set()
    for s in indo_sentences: indo_vocab.update(simple_tokenize(s))
    for s in kokas_sentences: kokas_vocab.update(simple_tokenize(s))
    
    print(f"--- Analisis: {name} Set ---")
    print(f"Jumlah Sampel: {num_samples}")
    if num_samples > 0:
        print(f"Rata-rata Kata (Indo): {statistics.mean(indo_lens):.2f} (Max: {max(indo_lens)}, Min: {min(indo_lens)})")
        print(f"Rata-rata Kata (Kokas): {statistics.mean(kokas_lens):.2f} (Max: {max(kokas_lens)}, Min: {min(kokas_lens)})")
    print(f"Jumlah Kosa Kata Unik (Indo): {len(indo_vocab)}")
    print(f"Jumlah Kosa Kata Unik (Kokas): {len(kokas_vocab)}")
    print("-" * 30)
    
    return set(indo_sentences), set(kokas_sentences)

print("=== LAPORAN EVALUASI DATASET (REVISI) ===\n")

sets_data = {}
for name, filename in files.items():
    path = os.path.join(dataset_dir, filename)
    if os.path.exists(path):
        sets_data[name] = analyze_split(name, path)

# Cek Overlap (Data Leakage) yang Sebenarnya
print("\n--- Pengecekan Kebocoran Data (Data Leakage) ---")
if 'Train' in sets_data and 'Test' in sets_data:
    train_indo = sets_data['Train'][0]
    test_indo = sets_data['Test'][0]
    overlap = train_indo.intersection(test_indo)
    print(f"Overlap Train vs Test (Kalimat Indo): {len(overlap)} kalimat")
    if len(overlap) > 0:
        print("PERINGATAN: Masih ada kebocoran!")
    else:
        print("SUKSES: Tidak ada kebocoran antara Train dan Test.")

if 'Train' in sets_data and 'Val' in sets_data:
    train_indo = sets_data['Train'][0]
    val_indo = sets_data['Val'][0]
    overlap = train_indo.intersection(val_indo)
    print(f"Overlap Train vs Val (Kalimat Indo): {len(overlap)} kalimat")
    if len(overlap) == 0:
        print("SUKSES: Tidak ada kebocoran antara Train dan Val.")
