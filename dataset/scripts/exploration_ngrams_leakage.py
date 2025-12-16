import csv
import collections
import re
import sys

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def get_ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def analyze_ngrams(file_path):
    print(f"\n--- Analisis N-Gram ({file_path}) ---")
    kokas_tokens = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'papua_kokas' in row:
                    kokas_tokens.extend(tokenize(row['papua_kokas']))
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
        return

    # Bigrams
    bigrams = get_ngrams(kokas_tokens, 2)
    bigram_counts = collections.Counter(bigrams)
    
    print(f"\n[Top 10 Bigrams - Bahasa Sekar]")
    for bg, count in bigram_counts.most_common(10):
        print(f"{bg[0]} {bg[1]:<15} : {count}")

    # Trigrams
    trigrams = get_ngrams(kokas_tokens, 3)
    trigram_counts = collections.Counter(trigrams)
    
    print(f"\n[Top 10 Trigrams - Bahasa Sekar]")
    for tg, count in trigram_counts.most_common(10):
        print(f"{tg[0]} {tg[1]} {tg[2]:<15} : {count}")


def check_leakage():
    print(f"\n--- Verifikasi Kebocoran Data (Data Leakage) ---")
    
    train_file = 'dataset/train.csv'
    test_file = 'dataset/test.csv'
    
    train_indo = set()
    test_indo = set()
    
    # Load Train
    try:
        with open(train_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                train_indo.add(row['indonesian'].strip().lower())
    except:
        print("Gagal membaca train.csv")
        return

    # Load Test
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_indo.add(row['indonesian'].strip().lower())
    except:
        print("Gagal membaca test.csv")
        return

    intersection = train_indo.intersection(test_indo)
    
    print(f"Jumlah Kalimat Unik Train: {len(train_indo)}")
    print(f"Jumlah Kalimat Unik Test : {len(test_indo)}")
    print(f"Jumlah Kalimat BOCOR     : {len(intersection)}")
    
    if len(intersection) > 0:
        print("PERINGATAN: Ditemukan kebocoran data!")
        print(list(intersection)[:5])
    else:
        print("SUKSES: Tidak ada kebocoran data (0 overlap). Metode strict splitting valid.")

if __name__ == "__main__":
    analyze_ngrams('dataset/master.csv')
    check_leakage()
