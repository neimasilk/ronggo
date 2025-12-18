import pandas as pd
import json
import re
import os

# Config
INPUT_CSV = "../train.csv"
OUTPUT_JSON = "../known_vocab.json"

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Lowercase, remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def build_vocab():
    print(f"Reading {INPUT_CSV}...")
    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    vocab_set = set()

    # Iterate over the 'papua_kokas' column
    if 'papua_kokas' not in df.columns:
        print("Error: Column 'papua_kokas' not found.")
        return

    print("Extracting vocabulary...")
    for sentence in df['papua_kokas']:
        cleaned = clean_text(sentence)
        words = cleaned.split()
        for word in words:
            if len(word) > 1: # Ignore single characters/noise
                vocab_set.add(word)

    # Convert to sorted list
    vocab_list = sorted(list(vocab_set))
    
    print(f"Found {len(vocab_list)} unique Sekar words.")
    
    # Save to JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({"valid_sekar_words": vocab_list}, f, indent=2, ensure_ascii=False)
    
    print(f"Vocabulary saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    build_vocab()
