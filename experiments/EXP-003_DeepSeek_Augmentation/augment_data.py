import os
import pandas as pd
import time
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Konfigurasi Path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../dataset/train.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "augmented_data_partial.csv")
FINAL_FILE = os.path.join(SCRIPT_DIR, "augmented_train_v1.csv")

# Konfigurasi API
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"

if not API_KEY:
    raise ValueError("API Key DeepSeek tidak ditemukan di .env!")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def get_paraphrases_batch(sentences):
    """Mengirim batch kalimat ke DeepSeek untuk diparafrase."""
    prompt = """
Tugasmu adalah melakukan parafrase (penulisan ulang) pada kalimat Bahasa Indonesia berikut agar strukturnya berbeda tapi maknanya TETAP SAMA PERSIS.
    Jangan ubah nama tempat, nama orang, atau istilah khusus.
    Gunakan bahasa Indonesia yang baku namun luwes.
    
    Format Output: Hanya berikan daftar kalimat hasil parafrase, satu per baris, tanpa penomoran.
    Urutan harus sesuai dengan input.
    
Daftar Kalimat:
    """
    
    input_text = "\n".join(sentences)
    full_prompt = prompt + input_text

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful linguistic assistant specializing in Indonesian paraphrasing."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        content = response.choices[0].message.content.strip()
        lines = content.split('\n')
        
        # Cleaning: Hapus numbering (1. , - )
        clean_lines = []
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Hapus angka/bullet di awal
            if line[0].isdigit() or line.startswith('-'):
                parts = line.split('.', 1) if line[0].isdigit() else line.split(' ', 1)
                if len(parts) > 1:
                    clean_lines.append(parts[1].strip())
                else:
                    clean_lines.append(line)
            else:
                clean_lines.append(line)
                    
        return clean_lines

    except Exception as e:
        print(f"Error API: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Augmentasi Data Bahasa Sekar menggunakan DeepSeek")
    parser.add_argument("--limit", type=int, default=None, help="Batasi jumlah data yang memproses (untuk testing)")
    parser.add_argument("--batch_size", type=int, default=20, help="Jumlah kalimat per request API")
    args = parser.parse_args()

    print("--- Memulai Augmentasi Data dengan DeepSeek ---")
    
    # Load Data Source
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Total Data Asli: {len(df)}")
    except FileNotFoundError:
        print(f"File {INPUT_FILE} tidak ditemukan.")
        return

    # Resume Logic
    augmented_rows = []
    processed_indices = set()
    
    # Cek partial file
    if os.path.exists(OUTPUT_FILE):
        try:
            existing_df = pd.read_csv(OUTPUT_FILE)
            augmented_rows = existing_df.to_dict('records')
            # Asumsi kita memproses berurutan, ambil jumlah data yang sudah ada / 2 (karena 1 asli + 1 aug)
            processed_count = len(existing_df) // 2
            print(f"Ditemukan file partial. Melanjutkan dari index {processed_count}...")
        except Exception as e:
            print(f"Warning: Gagal membaca file partial ({e}). Mulai dari awal.")

    start_idx = len(augmented_rows) // 2
    
    # Tentukan Limit Akhir
    total_rows = len(df)
    end_idx = total_rows
    if args.limit:
        end_idx = min(start_idx + args.limit, total_rows)
        print(f"Processing dibatasi hingga {args.limit} baris tambahan (Stop di index {end_idx}).")

    if start_idx >= end_idx:
        print("Target processing sudah tercapai atau selesai.")
    else:
        # Proses Batch
        source_sentences = df['indonesian'].tolist()
        target_sentences = df['papua_kokas'].tolist()
        
        for i in tqdm(range(start_idx, end_idx, args.batch_size)):
            batch_end = min(i + args.batch_size, end_idx)
            batch_src = source_sentences[i : batch_end]
            batch_tgt = target_sentences[i : batch_end]
            
            # Call API
            paraphrases = get_paraphrases_batch(batch_src)
            
            # Handling Mismatch (Jika LLM output kurang/lebih)
            if len(paraphrases) != len(batch_src):
                # print(f"\nWarning: Mismatch batch {i}. Input {len(batch_src)} vs Output {len(paraphrases)}. Menggunakan data asli sebagai fallback.")
                # Fallback: Gunakan kalimat asli jika gagal paraphrase agar data tidak hilang
                paraphrases = batch_src 

            # Simpan hasil
            for orig, para, tgt in zip(batch_src, paraphrases, batch_tgt):
                # Data 1: Hasil Augmentasi
                augmented_rows.append({
                    'indonesian_original': orig,
                    'indonesian': para, 
                    'papua_kokas': tgt,
                    'is_augmented': True
                })
                # Data 2: Data Asli
                augmented_rows.append({
                    'indonesian_original': orig,
                    'indonesian': orig,
                    'papua_kokas': tgt,
                    'is_augmented': False
                })
            
            # Save Partial setiap batch
            pd.DataFrame(augmented_rows).to_csv(OUTPUT_FILE, index=False)
            # time.sleep(0.5) # Sedikit delay untuk safety rate limit

    # Finalize jika sudah selesai semua (atau limit tercapai)
    final_df = pd.DataFrame(augmented_rows)
    print(f"\nMenyimpan hasil sementara/akhir ke {FINAL_FILE}...")
    final_df.to_csv(FINAL_FILE, index=False)
    print(f"Total data tersimpan: {len(final_df)} baris.")

if __name__ == "__main__":
    main()