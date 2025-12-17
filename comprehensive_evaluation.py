import pandas as pd
import torch
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm

# --- Konfigurasi ---
MODEL_PATH = "./nllb-sekar-finetuned/final_model"
TRAIN_PATH = "dataset/train.csv"
TEST_PATH = "dataset/test.csv"
SRC_LANG = "ind_Latn"
TGT_LANG = "eng_Latn" 
BATCH_SIZE = 32

def normalize(text):
    return str(text).lower().strip().replace('.', '').replace(',', '')

def main():
    print("--- EVALUASI MULTI-METRIC (BLEU, chrF, TER) ---")
    
    # 1. Load Data & Bersihkan Leakage
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    
    train_src_set = set(train_df['indonesian'].apply(normalize))
    clean_test_df = test_df[~test_df['indonesian'].apply(normalize).isin(train_src_set)].copy()
    
    print(f"Jumlah Data Test Bersih: {len(clean_test_df)}")
    
    # 2. Load Model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(TGT_LANG)

    # 3. Inferensi
    inputs = clean_test_df['indonesian'].tolist()
    # Format referensi untuk metrics: List of strings
    references = clean_test_df['papua_kokas'].tolist() 
    
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

    # 4. Hitung Metrics
    # Load metrics
    bleu = evaluate.load("bleu")
    chrf = evaluate.load("chrf")
    ter = evaluate.load("ter")
    
    print("\nMenghitung skor...")
    
    # BLEU (Standard)
    # Note: evaluate.load("bleu") expects references as list of list of strings for multiple refs per sample, 
    # but works with list of strings if 1 ref. Let's ensure format is [[ref], [ref]] for safety similar to sacrebleu.
    formatted_refs = [[r] for r in references]
    
    bleu_score = bleu.compute(predictions=predictions, references=formatted_refs)
    
    # chrF (Character level)
    chrf_score = chrf.compute(predictions=predictions, references=formatted_refs)
    
    # TER (Edit Distance - Lower is better)
    ter_score = ter.compute(predictions=predictions, references=formatted_refs)

    print("\n" + "="*40)
    print("HASIL EVALUASI KOMPREHENSIF")
    print("="*40)
    print(f"BLEU  : {bleu_score['bleu'] * 100:.2f}  (Akurasi Kata)") 
    print(f"chrF++: {chrf_score['score']:.2f}     (Akurasi Karakter/Morfologi)")
    print(f"TER   : {ter_score['score']:.2f}      (Tingkat Kesalahan - Lebih rendah lebih bagus)")
    print("="*40)
    
    # Interpretasi Sederhana
    print("\nInterpretasi:")
    print("- chrF biasanya lebih tinggi dari BLEU di bahasa daerah.")
    print("- TER di bawah 40-50 biasanya dianggap 'dapat dimengerti dengan sedikit edit'.")

if __name__ == "__main__":
    main()
