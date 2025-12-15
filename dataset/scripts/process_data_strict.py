import csv
import os
import re
import random

output_dir = 'dataset/clean_dataset'
os.makedirs(output_dir, exist_ok=True)

files_to_process = [
    {'path': 'dataset/2908_data.csv', 'inverted': True}, 
    {'path': 'dataset/data/Combined_Data.csv', 'inverted': False},
    {'path': 'dataset/data/data_id_ko.csv', 'inverted': False},
    {'path': 'dataset/data_2411.csv', 'inverted': False},
    {'path': 'dataset/data_1855.csv', 'inverted': False}
]

def clean_text(text):
    if not text: return ""
    # Hapus triple quotes, quotes biasa, dan spasi berlebih
    text = text.replace('"""', '').replace('"', '').replace("'", '').strip()
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower() # Lowercase untuk deduplikasi maksimal

# 1. Kumpulkan semua data mentah
raw_pairs = []

for item in files_to_process:
    path = item['path']
    if not os.path.exists(path):
        continue
    
    print(f"Reading {path}...")
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            for line in lines[1:]: # Skip header
                # Teknik split CSV manual yang lebih robust terhadap koma dalam quote
                # Tapi karena formatnya sederhana, kita coba bersihkan quote dulu
                # Asumsi: formatnya "kalimat1","kalimat2" atau kalimat1,kalimat2
                
                # Bersihkan format triple quote aneh dari file sumber
                line_clean = line.strip().replace('"""', '"')
                
                # Gunakan csv reader string untuk parsing baris
                reader = csv.reader([line_clean], skipinitialspace=True)
                for row in reader:
                    if len(row) >= 2:
                        if item['inverted']:
                            indo = clean_text(row[1])
                            kokas = clean_text(row[0])
                        else:
                            indo = clean_text(row[0])
                            kokas = clean_text(row[1])
                        
                        if indo and kokas:
                            raw_pairs.append({'indo': indo, 'kokas': kokas})
    except Exception as e:
        print(f"Error: {e}")

# 2. Deduplikasi Berbasis Kalimat Indonesia
# Kita group berdasarkan kalimat Indonesia untuk mencegah kebocoran di sisi source
unique_data_map = {} # Key: Indo, Value: List of Kokas translations

for pair in raw_pairs:
    indo = pair['indo']
    kokas = pair['kokas']
    
    if indo not in unique_data_map:
        unique_data_map[indo] = set()
    unique_data_map[indo].add(kokas)

print(f"Total Kalimat Indonesia Unik: {len(unique_data_map)}")

# 3. Flatten kembali menjadi list, pilih satu terjemahan jika ada duplikat (atau simpan semua)
# Untuk dataset machine translation sederhana, kita ambil satu pair unik (Indo, Kokas)
final_pairs = []
for indo, kokas_set in unique_data_map.items():
    for kokas in kokas_set:
        final_pairs.append((indo, kokas))

# Hapus duplikat total (jika ada overlap aneh)
final_pairs = list(set(final_pairs))
final_pairs.sort() # Deterministik
random.seed(42)
random.shuffle(final_pairs)

print(f"Total Pasangan Unik Akhir: {len(final_pairs)}")

# 4. Split Data (Strict Split berdasarkan Kalimat Indo agar tidak bocor)
# Kita split berdasarkan index list yang sudah di-shuffle
# Karena kita sudah deduplikasi dan shuffle, kita bisa potong langsung.
# Kuncinya: Data sudah unique pairs. 
# Catatan: Jika 1 kalimat Indo punya 2 terjemahan Kokas, keduanya akan berdekatan jika tidak di-shuffle,
# atau tersebar jika di-shuffle. Jika tersebar, Indo yang sama bisa masuk Train dan Test.
# JADI: Kita harus split berdasarkan KEY (Indo) nya dulu!

indo_keys = list(unique_data_map.keys())
indo_keys.sort()
random.shuffle(indo_keys)

n_total = len(indo_keys)
train_end = int(n_total * 0.8)
val_end = int(n_total * 0.9)

train_keys = set(indo_keys[:train_end])
val_keys = set(indo_keys[train_end:val_end])
test_keys = set(indo_keys[val_end:])

train_data = []
val_data = []
test_data = []

# Distribusikan pair berdasarkan key Indo-nya
for indo, kokas in final_pairs:
    if indo in train_keys:
        train_data.append((indo, kokas))
    elif indo in val_keys:
        val_data.append((indo, kokas))
    elif indo in test_keys:
        test_data.append((indo, kokas))

print(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")

# 5. Simpan
def save_csv(filename, data):
    with open(os.path.join(output_dir, filename), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['indonesian', 'papua_kokas'])
        writer.writerows(data)

save_csv('master.csv', final_pairs)
save_csv('train.csv', train_data)
save_csv('val.csv', val_data)
save_csv('test.csv', test_data)

print("Pemisahan data ketat selesai. Dijamin tidak ada kebocoran kalimat sumber.")
