from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_path = "./nllb-sekar-finetuned/final_model"
src_lang = "ind_Latn"
tgt_lang = "eng_Latn" # Placeholder for Sekar

print(f"Loading model from {model_path}...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Ensure correct language codes
tokenizer.src_lang = src_lang
tokenizer.tgt_lang = tgt_lang
forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

print(f"Model loaded on {device}.")

samples = [
    ("saya akan mengambil mobil ke bengkel besok.", "obisa eguain mobil ami bengkel utaf"),
    ("berapa lama perjalanan dari sini ke bandara", "parlu waktu firas parjalanan afi ege ati lapangan tarbang"),
    ("tolong beri tahu saya cara memesan tiket pesawat secara online", "tolong farok ati yai cara afno tiket kapal torbang secara online"),
    (". apa yang kamu ketahui tentang kebudayaan betawi?", "o bare kusafa adi kebudayaan betawi?"),
    ("apa rencanamu untuk akhir pekan ini?", "akape adi o rencana akhir pekan ige?")
]

print("\n--- Inference Results ---\n")

for src_text, ref_text in samples:
    inputs = tokenizer(src_text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=128
        )
    
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    
    print(f"Input:      {src_text}")
    print(f"Reference:  {ref_text}")
    print(f"Prediction: {result}")
    print("-" * 50)
