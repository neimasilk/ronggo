import pandas as pd
import torch
import evaluate
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm

# --- Konfigurasi ---
MODEL_PATH = "./nllb-sekar-finetuned/final_model"
TRAIN_PATH = "dataset/train.csv"
TEST_PATH = "dataset/test.csv"
SRC_LANG = "ind_Latn"
TGT_LANG = "eng_Latn" # Placeholder untuk Sekar
BATCH_SIZE = 16

def normalize(text):
    return str(text).lower().strip().replace('.', '').replace(',', '')

def main():
    print("--- MULAI EVALUASI ULANG (CLEAN TEST SET) ---")
    
    # 1. Load Data & Bersihkan Leakage
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    
    # Identifikasi Leakage
    train_src_set = set(train_df['indonesian'].apply(normalize))
    
    # Filter Test Set: Hanya ambil yang TIDAK ada di training
    clean_test_df = test_df[~test_df['indonesian'].apply(normalize).isin(train_src_set)].copy()
    
    original_count = len(test_df)
    clean_count = len(clean_test_df)
    removed_count = original_count - clean_count
    
    print(f"Data Test Awal: {original_count}")
    print(f"Data Test Bersih: {clean_count} (Dibuang {removed_count} kalimat bocor)")
    
    if clean_count == 0:
        print("Error: Tidak ada data tersisa setelah pembersihan!")
        return

    # 2. Load Model & Tokenizer
    print(f"\nLoading model dari {MODEL_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    
    tokenizer.src_lang = SRC_LANG
    tokenizer.tgt_lang = TGT_LANG
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(TGT_LANG)

    # 3. Inferensi Batch
    inputs = clean_test_df['indonesian'].tolist()
    references = [[ref] for ref in clean_test_df['papua_kokas'].tolist()] # Format referensi sacrebleu
    
    predictions = []
    
    print("Melakukan inferensi...")
    for i in tqdm(range(0, len(inputs), BATCH_SIZE)):
        batch_inputs = inputs[i : i + BATCH_SIZE]
        
        model_inputs = tokenizer(batch_inputs, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
        
        with torch.no_grad():
            generated_tokens = model.generate(
                **model_inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=128
            )
            
        decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        predictions.extend([pred.strip() for pred in decoded_preds])

    # 4. Hitung BLEU
    metric = evaluate.load("sacrebleu")
    
    # Tampilkan beberapa contoh
    print("\n--- Contoh Hasil (Clean) ---")
    for i in range(5):
        print(f"SRC: {inputs[i]}")
        print(f"REF: {references[i][0]}")
        print(f"PRED: {predictions[i]}")
        print("-" * 20)

    result = metric.compute(predictions=predictions, references=references)
    
    print("\n" + "="*40)
    print(f"SKOR BLEU JUJUR (Clean Test Set): {result['score']:.2f}")
    print("="*40)

if __name__ == "__main__":
    main()
