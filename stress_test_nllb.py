from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_path = "./nllb-sekar-finetuned/final_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

tokenizer.src_lang = "ind_Latn"
tokenizer.tgt_lang = "eng_Latn" # Placeholder Sekar
forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")

# KUMPULAN KALIMAT JEBAKAN
stress_samples = [
    # 1. Syntactic Stress (Kata umum, struktur dibalik)
    # Hipotesis: Jika model overfit, dia akan membetulkan logika kalimatnya ("Bapak makan ikan")
    ("Ikan itu memakan bapak saya.", "Syntactic Check (Subject-Object Swap)"),
    
    ("Anjing tidur di atas laut.", "Semantic Nonsense (Valid Grammar)"),

    # 2. Modern/Out-of-Domain (Kata yang mungkin tidak ada di data adat)
    ("Saya sedang memperbaiki komputer yang rusak.", "Modern Context"),
    ("Presiden jokowi meresmikan jalan tol.", "Specific Entity"),
    
    # 3. Complex Combination
    ("Walaupun hujan turun sangat deras, dia tetap pergi ke sekolah tanpa payung.", "Complex Logic")
]

print("--- STRESS TEST: MENGUJI KECERDASAN VS HAFALAN ---")

for src_text, label in stress_samples:
    inputs = tokenizer(src_text, return_tensors="pt").to(device)
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=128
        )
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    
    print(f"Type:  {label}")
    print(f"Input: {src_text}")
    print(f"Pred:  {result}")
    print("-" * 40)
