import os
import csv
import random
import json
import argparse
import pandas as pd
from typing import List, Dict

# Try importing libraries
try:
    import google.generativeai as genai
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError:
    print("Error: Missing libraries. Please install them:")
    print("pip install google-generativeai openai pandas python-dotenv")
    exit(1)

# Load environment variables from .env file (if exists, mostly for Local PC)
load_dotenv()

# Configuration
DATASET_PATH = "../train.csv"
VOCAB_PATH = "../known_vocab.json"
OUTPUT_DIR = "../synthetic/"

def load_vocab(file_path: str) -> str:
    """Loads the whitelist of valid Sekar words."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            words = data.get("valid_sekar_words", [])
            # Join them into a string for the prompt
            return ", ".join(words)
    except Exception as e:
        print(f"Warning: Could not load vocabulary from {file_path}. ({e})")
        return ""

def load_examples(file_path: str, n: int = 10) -> str:
    """Loads random examples from the training CSV to use as few-shot prompts."""
    try:
        df = pd.read_csv(file_path)
        if 'indonesian' not in df.columns or 'papua_kokas' not in df.columns:
            raise ValueError("CSV must contain 'indonesian' and 'papua_kokas' columns.")
        
        sample = df.sample(n=min(n, len(df)))
        examples_text = ""
        for _, row in sample.iterrows():
            examples_text += f"Indonesian: {row['indonesian']}\nSekar: {row['papua_kokas']}\n---\n"
        return examples_text
    except Exception as e:
        print(f"Error loading examples: {e}")
        return ""

def generate_prompt(examples: str, vocab_list: str, count: int = 10) -> str:
    """Constructs the prompt for the LLM with strict vocabulary constraints."""
    
    return f"""
You are a linguistic expert assisting in creating a dataset for the Sekar (Kokas) language of Papua, Indonesia.
The Sekar language is heavily influenced by Indonesian.

Your task is to generate {count} NEW pairs of sentences (Indonesian -> Sekar).

### CRITICAL RESOURCE (VOCABULARY WHITELIST):
The following is the COMPLETE list of valid Sekar words known to us.
[{vocab_list}]

### RULES (STRICT ENFORCEMENT):
1.  **VOCABULARY CHECK (The "Dictionary Rule"):**
    *   When translating to Sekar, check the WHITELIST above.
    *   If a word exists in the whitelist -> USE IT.
    *   If a word DOES NOT exist in the whitelist -> **USE THE ORIGINAL INDONESIAN WORD**.
    *   **DO NOT INVENT WORDS.** Do not try to guess Sekar morphology if you haven't seen it.
2.  **NER PRESERVATION:**
    *   Do NOT translate Names, Cities, Countries. Keep them EXACTLY as in Indonesian.
3.  **COMPLEXITY:**
    *   The Indonesian sentences must be **compound/complex sentences** (using "dan", "tetapi", "karena", "walaupun").
    *   Mix Indonesian words freely into the Sekar sentence following Rule #1. This is "Code Mixing" and is desired.

### EXAMPLES (Style Reference):
{examples}

### OUTPUT FORMAT:
Generate exactly {count} pairs.
Format:
Indonesian Sentence | Sekar Sentence

Do not add numbering, explanations, or introductory text. Just the raw CSV-like lines.
"""

def generate_with_gemini(api_key: str, prompt: str) -> str:
    """Generates text using Google's Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Use Flash for speed/cost/context
    response = model.generate_content(prompt)
    return response.text

def generate_with_deepseek(api_key: str, prompt: str) -> str:
    """Generates text using DeepSeek."""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful linguistic assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content

def save_to_csv(data: str, filename: str):
    rows = []
    lines = data.strip().split('\n')
    for line in lines:
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                ind = parts[0].strip()
                sekar = parts[1].strip()
                rows.append({'indonesian': ind, 'papua_kokas': sekar})
    
    if not rows:
        print("Warning: No valid rows parsed from LLM output.")
        print("Raw Output:", data)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, filename)
    mode = 'a' if os.path.exists(out_path) else 'w'
    header = not os.path.exists(out_path)
    pd.DataFrame(rows).to_csv(out_path, mode=mode, header=header, index=False)
    print(f"Successfully saved {len(rows)} pairs to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic training data using LLMs.")
    parser.add_argument("--provider", choices=["gemini", "deepseek"], required=True, help="LLM Provider to use")
    parser.add_argument("--key", type=str, help="API Key (Optional if set in .env)")
    parser.add_argument("--count", type=int, default=10, help="Number of sentences to generate per run")
    parser.add_argument("--batch", type=str, default="batch_1.csv", help="Output filename")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt and exit without calling API")
    
    args = parser.parse_args()
    
    # API Key Logic: Arg > Env > Error
    api_key = args.key
    if not api_key and not args.dry_run:
        if args.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
        elif args.provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            
        if not api_key:
            print(f"Error: API Key for {args.provider} is missing.")
            print("Provide it via --key argument OR set GEMINI_API_KEY / DEEPSEEK_API_KEY in .env file")
            return

    # 1. Build Dictionary if missing
    if not os.path.exists(VOCAB_PATH):
        print(f"Vocabulary file not found at {VOCAB_PATH}. Please run 'build_dictionary.py' first.")
        # Optional: Auto-run it? Let's just warn for now to keep steps clear.
        return

    print(f"Loading vocabulary from {VOCAB_PATH}...")
    vocab_list = load_vocab(VOCAB_PATH)
    if not vocab_list:
        print("Vocabulary is empty. Exiting.")
        return

    print(f"Loading examples from {DATASET_PATH}...")
    examples = load_examples(DATASET_PATH)

    print("Constructing prompt with Vocabulary Constraint...")
    prompt = generate_prompt(examples, vocab_list, args.count)
    
    # DRY RUN CHECK
    if args.dry_run:
        print("\n" + "="*40)
        print(" [DRY RUN MODE] GENERATED PROMPT PREVIEW ")
        print("="*40)
        print(prompt)
        print("="*40)
        print("Dry run complete. No API call made.")
        return

    print(f"Sending request to {args.provider}...")
    try:
        if args.provider == "gemini":
            result = generate_with_gemini(api_key, prompt)
        elif args.provider == "deepseek":
            result = generate_with_deepseek(api_key, prompt)
        
        print("Processing response...")
        save_to_csv(result, args.batch)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()