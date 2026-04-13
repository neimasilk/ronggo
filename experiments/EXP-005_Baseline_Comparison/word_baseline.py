"""
Word-based Dictionary Baseline for Indonesian-Papua Kokas Translation

This baseline translates word-by-word using a dictionary built from training data.
It serves as a lower-bound comparison for neural approaches.

Author: EXP-005 Baseline Comparison
"""

import pandas as pd
import evaluate
from collections import defaultdict
from tqdm import tqdm
import json
import os

# Configuration
TRAIN_PATH = "../../dataset/train.csv"
TEST_PATH = "../../dataset/test.csv"
OUTPUT_DIR = "./results"

def normalize(text):
    """Normalize text for comparison."""
    return str(text).lower().strip().replace('.', '').replace(',', '').replace('?', '').replace('!', '')

def build_word_dictionary(train_df):
    """
    Build word-to-word translation dictionary from training data.
    For each Indonesian word, find the most common Papua Kokas translation.
    """
    word_pairs = defaultdict(lambda: defaultdict(int))

    for _, row in train_df.iterrows():
        src_words = normalize(row['indonesian']).split()
        tgt_words = normalize(row['papua_kokas']).split()

        # Simple word alignment: assume similar word order
        # Use zip to pair words (handles different lengths)
        for src, tgt in zip(src_words, tgt_words):
            word_pairs[src][tgt] += 1

    # Select most common translation for each word
    dictionary = {}
    for src_word, translations in word_pairs.items():
        best_translation = max(translations.items(), key=lambda x: x[1])
        dictionary[src_word] = best_translation[0]

    return dictionary

def translate_sentence(sentence, dictionary):
    """Translate a sentence word by word using the dictionary."""
    words = normalize(sentence).split()
    translated = []

    for word in words:
        if word in dictionary:
            translated.append(dictionary[word])
        else:
            # OOV: copy the word as-is
            translated.append(word)

    return ' '.join(translated)

def evaluate_baseline(predictions, references):
    """Evaluate using BLEU, chrF, and TER metrics."""
    bleu = evaluate.load("bleu")
    chrf = evaluate.load("chrf")
    ter = evaluate.load("ter")

    # Format references as list of lists
    formatted_refs = [[r] for r in references]

    bleu_score = bleu.compute(predictions=predictions, references=formatted_refs)
    chrf_score = chrf.compute(predictions=predictions, references=formatted_refs)
    ter_score = ter.compute(predictions=predictions, references=formatted_refs)

    return {
        'bleu': bleu_score['bleu'] * 100,
        'chrf': chrf_score['score'],
        'ter': ter_score['score']
    }

def main():
    print("=" * 50)
    print("WORD-BASED DICTIONARY BASELINE")
    print("=" * 50)

    # Load data
    print("\n1. Loading data...")
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    print(f"   Train samples: {len(train_df)}")
    print(f"   Test samples: {len(test_df)}")

    # Build dictionary
    print("\n2. Building word dictionary from training data...")
    dictionary = build_word_dictionary(train_df)
    print(f"   Dictionary size: {len(dictionary)} words")

    # Save dictionary for inspection
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, 'word_dictionary.json'), 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
    print(f"   Dictionary saved to {OUTPUT_DIR}/word_dictionary.json")

    # Translate test set
    print("\n3. Translating test set...")
    predictions = []
    references = test_df['papua_kokas'].apply(normalize).tolist()

    for _, row in tqdm(test_df.iterrows(), total=len(test_df)):
        pred = translate_sentence(row['indonesian'], dictionary)
        predictions.append(pred)

    # Evaluate
    print("\n4. Evaluating...")
    scores = evaluate_baseline(predictions, references)

    # Print results
    print("\n" + "=" * 50)
    print("RESULTS: WORD-BASED BASELINE")
    print("=" * 50)
    print(f"BLEU:   {scores['bleu']:.2f}")
    print(f"chrF++: {scores['chrf']:.2f}")
    print(f"TER:    {scores['ter']:.2f}")
    print("=" * 50)

    # Save results
    results = {
        'model': 'Word-based Dictionary',
        'architecture': 'Dictionary Lookup',
        'bleu': round(scores['bleu'], 2),
        'chrf': round(scores['chrf'], 2),
        'ter': round(scores['ter'], 2),
        'dictionary_size': len(dictionary),
        'test_samples': len(test_df)
    }

    with open(os.path.join(OUTPUT_DIR, 'word_baseline_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {OUTPUT_DIR}/word_baseline_results.json")

    # Show sample translations
    print("\n" + "=" * 50)
    print("SAMPLE TRANSLATIONS")
    print("=" * 50)
    for i in range(min(5, len(test_df))):
        src = test_df.iloc[i]['indonesian']
        ref = test_df.iloc[i]['papua_kokas']
        pred = predictions[i]
        print(f"\nSource:     {src}")
        print(f"Reference:  {ref}")
        print(f"Prediction: {pred}")

    return scores

if __name__ == "__main__":
    main()
