"""
Unified Evaluation Script for All Models

This script evaluates and compares all translation models:
1. Word-based Dictionary Baseline
2. LSTM Seq2Seq with Attention
3. NLLB-200 (Transformer)

Output: Comparison table in CSV format for paper.

Author: EXP-005 Baseline Comparison
"""

import pandas as pd
import torch
import evaluate
import json
import os
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Import baseline modules
from word_baseline import build_word_dictionary, translate_sentence, normalize
from lstm_seq2seq import (
    Vocabulary, Seq2Seq, Encoder, Decoder,
    EMBEDDING_DIM, HIDDEN_DIM, NUM_LAYERS, DROPOUT, MIN_FREQ,
    SOS_TOKEN, EOS_TOKEN
)

# Configuration
TRAIN_PATH = "../../dataset/train.csv"
TEST_PATH = "../../dataset/test.csv"
NLLB_MODEL_PATH = "../../nllb-sekar-finetuned/final_model"
LSTM_MODEL_PATH = "./lstm_model/best_model.pt"
OUTPUT_DIR = "./results"

TGT_LANG = "eng_Latn"  # Placeholder for Papua Kokas in NLLB


def evaluate_metrics(predictions, references):
    """Compute BLEU, chrF++, and TER metrics."""
    bleu = evaluate.load("bleu")
    chrf = evaluate.load("chrf")
    ter = evaluate.load("ter")

    # Normalize predictions and references
    preds_normalized = [p.lower().strip() for p in predictions]
    refs_normalized = [[r.lower().strip()] for r in references]

    bleu_score = bleu.compute(predictions=preds_normalized, references=refs_normalized)
    chrf_score = chrf.compute(predictions=preds_normalized, references=refs_normalized)
    ter_score = ter.compute(predictions=preds_normalized, references=refs_normalized)

    return {
        'BLEU': round(bleu_score['bleu'] * 100, 2),
        'chrF++': round(chrf_score['score'], 2),
        'TER': round(ter_score['score'], 2)
    }


def evaluate_word_baseline(train_df, test_df):
    """Evaluate word-based dictionary baseline."""
    print("\n" + "=" * 50)
    print("Evaluating: WORD-BASED DICTIONARY BASELINE")
    print("=" * 50)

    dictionary = build_word_dictionary(train_df)
    predictions = []

    for _, row in tqdm(test_df.iterrows(), total=len(test_df)):
        pred = translate_sentence(row['indonesian'], dictionary)
        predictions.append(pred)

    references = test_df['papua_kokas'].apply(normalize).tolist()
    return evaluate_metrics(predictions, references)


def evaluate_lstm_seq2seq(train_df, test_df, device):
    """Evaluate LSTM Seq2Seq model."""
    print("\n" + "=" * 50)
    print("Evaluating: LSTM SEQ2SEQ WITH ATTENTION")
    print("=" * 50)

    if not os.path.exists(LSTM_MODEL_PATH):
        print("   WARNING: LSTM model not found. Run lstm_seq2seq.py first.")
        return {'BLEU': None, 'chrF++': None, 'TER': None}

    # Build vocabularies
    src_vocab = Vocabulary(min_freq=MIN_FREQ)
    tgt_vocab = Vocabulary(min_freq=MIN_FREQ)
    src_vocab.build(train_df['indonesian'].tolist())
    tgt_vocab.build(train_df['papua_kokas'].tolist())

    # Load model
    encoder = Encoder(len(src_vocab), EMBEDDING_DIM, HIDDEN_DIM, NUM_LAYERS, DROPOUT)
    decoder = Decoder(len(tgt_vocab), EMBEDDING_DIM, HIDDEN_DIM, NUM_LAYERS, DROPOUT)
    model = Seq2Seq(encoder, decoder, device).to(device)
    model.load_state_dict(torch.load(LSTM_MODEL_PATH, map_location=device))
    model.eval()

    # Translate
    predictions = []
    for _, row in tqdm(test_df.iterrows(), total=len(test_df)):
        src = torch.tensor([src_vocab.encode(row['indonesian'])]).to(device)
        output_indices = model.translate(
            src,
            sos_idx=tgt_vocab.word2idx[SOS_TOKEN],
            eos_idx=tgt_vocab.word2idx[EOS_TOKEN]
        )
        prediction = tgt_vocab.decode(output_indices)
        predictions.append(prediction)

    references = test_df['papua_kokas'].tolist()
    return evaluate_metrics(predictions, references)


def evaluate_nllb_transformer(test_df, device):
    """Evaluate NLLB-200 Transformer model."""
    print("\n" + "=" * 50)
    print("Evaluating: NLLB-200 (TRANSFORMER)")
    print("=" * 50)

    if not os.path.exists(NLLB_MODEL_PATH):
        print("   WARNING: NLLB model not found at", NLLB_MODEL_PATH)
        return {'BLEU': None, 'chrF++': None, 'TER': None}

    # Load model
    tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL_PATH).to(device)
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(TGT_LANG)

    # Translate in batches
    predictions = []
    batch_size = 32

    for i in tqdm(range(0, len(test_df), batch_size)):
        batch_inputs = test_df['indonesian'].iloc[i:i+batch_size].tolist()
        model_inputs = tokenizer(
            batch_inputs,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        ).to(device)

        with torch.no_grad():
            generated_tokens = model.generate(
                **model_inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=128
            )

        decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        predictions.extend([pred.strip() for pred in decoded_preds])

    references = test_df['papua_kokas'].tolist()
    return evaluate_metrics(predictions, references)


def main():
    print("=" * 60)
    print("UNIFIED MODEL EVALUATION")
    print("=" * 60)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load data
    print("\nLoading data...")
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)
    print(f"Test samples: {len(test_df)}")

    # Evaluate all models
    results = []

    # 1. Word Baseline
    word_scores = evaluate_word_baseline(train_df, test_df)
    results.append({
        'Model': 'Word Baseline',
        'Architecture': 'Dictionary Lookup',
        **word_scores
    })

    # 2. LSTM Seq2Seq
    lstm_scores = evaluate_lstm_seq2seq(train_df, test_df, device)
    results.append({
        'Model': 'LSTM Seq2Seq',
        'Architecture': 'Bi-LSTM + Attention',
        **lstm_scores
    })

    # 3. NLLB-200 Transformer
    nllb_scores = evaluate_nllb_transformer(test_df, device)
    results.append({
        'Model': 'NLLB-200',
        'Architecture': 'Transformer',
        **nllb_scores
    })

    # Create comparison table
    results_df = pd.DataFrame(results)

    # Print table
    print("\n" + "=" * 70)
    print("COMPARISON TABLE: Model Performance on Indonesian-Papua Kokas Translation")
    print("=" * 70)
    print(results_df.to_string(index=False))
    print("=" * 70)

    # Save results
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # CSV for paper
    results_df.to_csv(os.path.join(OUTPUT_DIR, 'comparison_table.csv'), index=False)
    print(f"\nResults saved to {OUTPUT_DIR}/comparison_table.csv")

    # JSON for detailed analysis
    with open(os.path.join(OUTPUT_DIR, 'all_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Detailed results saved to {OUTPUT_DIR}/all_results.json")

    # Print summary for paper
    print("\n" + "=" * 70)
    print("SUMMARY FOR PAPER")
    print("=" * 70)
    print("""
Table X: Comparison of Translation Methods on Indonesian-Papua Kokas Dataset

| Model          | Architecture          | BLEU  | chrF++ | TER   |
|----------------|----------------------|-------|--------|-------|""")

    for r in results:
        bleu = f"{r['BLEU']:.2f}" if r['BLEU'] else "N/A"
        chrf = f"{r['chrF++']:.2f}" if r['chrF++'] else "N/A"
        ter = f"{r['TER']:.2f}" if r['TER'] else "N/A"
        print(f"| {r['Model']:<14} | {r['Architecture']:<20} | {bleu:<5} | {chrf:<6} | {ter:<5} |")

    return results_df


if __name__ == "__main__":
    main()
