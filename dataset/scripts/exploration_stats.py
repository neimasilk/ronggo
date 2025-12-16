import csv
import collections
import re
import sys

# Konfigurasi
DATA_PATH = 'dataset/master.csv'

def tokenize(text):
    """Tokenisasi sederhana: lowercase dan split spasi, hapus tanda baca dasar."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Hapus tanda baca
    return text.split()

def analyze_stats(file_path):
    print(f"--- Menganalisis {file_path} ---")
    
    indo_tokens = []
    kokas_tokens = []
    pair_count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pair_count += 1
                if 'indonesian' in row and 'papua_kokas' in row:
                    indo_tokens.extend(tokenize(row['indonesian']))
                    kokas_tokens.extend(tokenize(row['papua_kokas']))
    except FileNotFoundError:
        print(f"File tidak ditemukan: {file_path}")
        return

    # Statistik Dasar
    print(f"\n1. STATISTIK DASAR")
    print(f"Total Pasangan Kalimat: {pair_count}")
    
    avg_indo = len(indo_tokens) / pair_count if pair_count else 0
    avg_kokas = len(kokas_tokens) / pair_count if pair_count else 0
    
    print(f"Rata-rata Panjang Kalimat (Kata) - Indo : {avg_indo:.2f}")
    print(f"Rata-rata Panjang Kalimat (Kata) - Kokas: {avg_kokas:.2f}")
    
    # Vocabulary
    indo_vocab = set(indo_tokens)
    kokas_vocab = set(kokas_tokens)
    
    print(f"Ukuran Kosakata (Unique Words) - Indo : {len(indo_vocab)}")
    print(f"Ukuran Kosakata (Unique Words) - Kokas: {len(kokas_vocab)}")
    
    # Rasio TTR (Type-Token Ratio) - Indikator kekayaan leksikal
    # Semakin rendah TTR, semakin repetitif teksnya (ciri dataset template)
    ttr_indo = len(indo_vocab) / len(indo_tokens) if indo_tokens else 0
    ttr_kokas = len(kokas_vocab) / len(kokas_tokens) if kokas_tokens else 0
    
    print(f"Type-Token Ratio (TTR) - Indo : {ttr_indo:.4f}")
    print(f"Type-Token Ratio (TTR) - Kokas: {ttr_kokas:.4f}")

    # Frekuensi Kata (Top 20)
    print(f"\n2. TOP 20 KATA TERSERING")
    
    indo_counts = collections.Counter(indo_tokens)
    kokas_counts = collections.Counter(kokas_tokens)
    
    print("\n[Bahasa Indonesia]")
    print(f"{'Kata':<15} {'Frekuensi':<10}")
    print("-" * 25)
    for word, count in indo_counts.most_common(20):
        print(f"{word:<15} {count:<10}")
        
    print("\n[Bahasa Sekar (Kokas)]")
    print(f"{'Kata':<15} {'Frekuensi':<10}")
    print("-" * 25)
    for word, count in kokas_counts.most_common(20):
        print(f"{word:<15} {count:<10}")

if __name__ == "__main__":
    analyze_stats(DATA_PATH)
