import pandas as pd
import collections
import os

# Konfigurasi Path (Relatif terhadap root project, diasumsikan script dijalankan dari root atau handled by path logic)
# Kita gunakan path absolut/relatif yang aman
BASE_DIR = os.getcwd()
TRAIN_PATH = os.path.join(BASE_DIR, 'dataset', 'train.csv')
TEST_PATH = os.path.join(BASE_DIR, 'dataset', 'test.csv')
OUTPUT_REPORT = os.path.join(BASE_DIR, 'experiments', 'EXP-002_NGram_Analysis', 'REPORT.md')

def get_ngrams(text, n):
    """Menghasilkan list n-gram dari teks string."""
    if not isinstance(text, str):
        return []
    # Normalisasi sederhana: lowercase & hapus tanda baca dasar
    text = text.lower().replace('.', '').replace(',', '').replace('?', '').replace('!', '')
    tokens = text.split()
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def analyze_overlap(train_df, test_df, column_name, n_range=[1, 2, 3, 4]):
    results = {}
    
    print(f"Mengumpulkan N-Grams untuk kolom '{column_name}'...")
    
    # Kumpulkan semua n-gram dari Training Data
    train_ngrams = {n: set() for n in n_range}
    for text in train_df[column_name]:
        for n in n_range:
            grams = get_ngrams(text, n)
            train_ngrams[n].update(grams)
            
    # Analisis Test Data
    stats = {n: {'total_test_grams': 0, 'overlap_count': 0} for n in n_range}
    
    for text in test_df[column_name]:
        for n in n_range:
            grams = get_ngrams(text, n)
            if not grams: continue
            
            stats[n]['total_test_grams'] += len(grams)
            for g in grams:
                if g in train_ngrams[n]:
                    stats[n]['overlap_count'] += 1
    
    return stats

def write_report(stats_src, stats_tgt):
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# Laporan Eksperimen EXP-002: Analisis Overlap N-Gram\n\n")
        f.write("**Tanggal:** 29 Januari 2026\n")
        f.write("**Tujuan:** Memvalidasi independensi dataset Test terhadap Train. Skor BLEU yang tinggi mencurigakan jika overlap N-Gram terlalu tinggi.\n\n")
        
        f.write("## 1. Analisis Bahasa Indonesia (Source)\n")
        f.write("Seberapa mirip kalimat input di Test dengan Train?\n\n")
        f.write("| N-Gram | Total di Test | Overlap (Hafalan) | % Overlap | Status |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        for n, data in stats_src.items():
            pct = (data['overlap_count'] / data['total_test_grams'] * 100) if data['total_test_grams'] > 0 else 0
            status = "⚠️ BAHAYA" if pct > 70 else "⚠️ WASPADA" if pct > 50 else "✅ AMAN"
            f.write(f"| {n}-gram | {data['total_test_grams']} | {data['overlap_count']} | **{pct:.2f}%** | {status} |\n")
            
        f.write("\n## 2. Analisis Bahasa Sekar (Target)\n")
        f.write("Seberapa mirip kalimat output yang diharapkan di Test dengan Train?\n\n")
        f.write("| N-Gram | Total di Test | Overlap (Hafalan) | % Overlap | Status |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        for n, data in stats_tgt.items():
            pct = (data['overlap_count'] / data['total_test_grams'] * 100) if data['total_test_grams'] > 0 else 0
            status = "⚠️ BAHAYA" if pct > 70 else "⚠️ WASPADA" if pct > 50 else "✅ AMAN"
            f.write(f"| {n}-gram | {data['total_test_grams']} | {data['overlap_count']} | **{pct:.2f}%** | {status} |\n")

        f.write("\n## 3. Kesimpulan\n")
        f.write("Jika overlap pada 3-gram dan 4-gram melebihi 50%, maka sebagian besar frasa yang diuji sebenarnya sudah pernah dilihat model saat training. Ini menjelaskan kenapa BLEU score tinggi.\n")

def main():
    print("--- Memulai Analisis N-Gram (EXP-002) ---")
    
    try:
        train_df = pd.read_csv(TRAIN_PATH)
        test_df = pd.read_csv(TEST_PATH)
    except FileNotFoundError:
        print("Error: Tidak bisa menemukan file dataset.")
        return

    print(f"Data Train: {len(train_df)} baris")
    print(f"Data Test: {len(test_df)} baris")
    
    # Analisis Source (Indonesia)
    print("\nMenganalisis Source (Indonesia)...")
    stats_src = analyze_overlap(train_df, test_df, 'indonesian')
    
    # Analisis Target (Sekar)
    print("Menganalisis Target (Papua Kokas)...")
    stats_tgt = analyze_overlap(train_df, test_df, 'papua_kokas')
    
    write_report(stats_src, stats_tgt)
    print(f"\nSelesai! Laporan disimpan di: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
