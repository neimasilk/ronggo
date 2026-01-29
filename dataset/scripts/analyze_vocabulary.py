import pandas as pd
import collections
import re

def tokenize(text):
    if not isinstance(text, str): return []
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def main():
    print("--- Analisis Kosakata Bahasa Sekar ---")
    
    try:
        df = pd.read_csv("dataset/master.csv")
    except:
        print("Gagal membaca dataset/master.csv")
        return

    all_tokens = []
    for text in df['papua_kokas']:
        all_tokens.extend(tokenize(text))

    counter = collections.Counter(all_tokens)
    total_unique = len(counter)
    total_words = sum(counter.values())

    print(f"Total Kata (Tokens): {total_words}")
    print(f"Total Kosakata Unik (Types): {total_unique}")

    # Kata Paling Sering
    print("\n[Top 20 Kata Paling Sering]")
    for word, count in counter.most_common(20):
        print(f"{word:<15} : {count}")

    # Hapax Legomena (Kata yang hanya muncul 1 kali)
    hapax = [word for word, count in counter.items() if count == 1]
    print(f"\nJumlah Kata Unik (Muncul 1x): {len(hapax)} ({len(hapax)/total_unique*100:.2f}%)")
    
    print("\nContoh Kata Langka (Hapax):")
    print(", ".join(hapax[:30]))

    # Simpan ke file untuk referensi pembuatan Hard Test Set
    with open("dataset/rare_words_sekar.txt", "w", encoding="utf-8") as f:
        f.write("# Daftar Kata Langka Bahasa Sekar (Muncul < 3x)\n")
        for word, count in sorted(counter.items(), key=lambda x: x[1]):
            if count < 3:
                f.write(f"{word} ({count})\n")
    
    print(f"\nDaftar lengkap kata langka disimpan di dataset/rare_words_sekar.txt")

if __name__ == "__main__":
    main()
