"""
LSTM Seq2Seq with Attention Baseline for Indonesian-Papua Kokas Translation

This implements a classic encoder-decoder LSTM architecture with Bahdanau attention,
representing the pre-Transformer era of Neural Machine Translation.

Author: EXP-005 Baseline Comparison
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import pandas as pd
import numpy as np
import evaluate
from collections import Counter
from tqdm import tqdm
import json
import os
import random

# Set seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)

# Configuration
TRAIN_PATH = "../../dataset/train.csv"
VAL_PATH = "../../dataset/val.csv"
TEST_PATH = "../../dataset/test.csv"
OUTPUT_DIR = "./results"
MODEL_DIR = "./lstm_model"

# Hyperparameters (tuned for small dataset)
EMBEDDING_DIM = 256
HIDDEN_DIM = 512
NUM_LAYERS = 2
DROPOUT = 0.3
BATCH_SIZE = 32
LEARNING_RATE = 0.001
NUM_EPOCHS = 100
PATIENCE = 10  # Early stopping patience
MIN_FREQ = 2   # Minimum word frequency for vocabulary

# Special tokens
PAD_TOKEN = '<pad>'
UNK_TOKEN = '<unk>'
SOS_TOKEN = '<sos>'
EOS_TOKEN = '<eos>'

class Vocabulary:
    """Vocabulary class for mapping words to indices."""

    def __init__(self, min_freq=1):
        self.min_freq = min_freq
        self.word2idx = {}
        self.idx2word = {}
        self.word_count = Counter()

    def build(self, sentences):
        """Build vocabulary from sentences."""
        for sent in sentences:
            self.word_count.update(sent.lower().split())

        # Add special tokens
        self.word2idx = {
            PAD_TOKEN: 0,
            UNK_TOKEN: 1,
            SOS_TOKEN: 2,
            EOS_TOKEN: 3
        }

        # Add words meeting frequency threshold
        idx = 4
        for word, count in self.word_count.items():
            if count >= self.min_freq:
                self.word2idx[word] = idx
                idx += 1

        self.idx2word = {v: k for k, v in self.word2idx.items()}

    def encode(self, sentence):
        """Convert sentence to indices."""
        words = sentence.lower().split()
        return [self.word2idx.get(w, self.word2idx[UNK_TOKEN]) for w in words]

    def decode(self, indices):
        """Convert indices back to words."""
        words = []
        for idx in indices:
            if idx == self.word2idx[EOS_TOKEN]:
                break
            if idx not in [self.word2idx[PAD_TOKEN], self.word2idx[SOS_TOKEN]]:
                words.append(self.idx2word.get(idx, UNK_TOKEN))
        return ' '.join(words)

    def __len__(self):
        return len(self.word2idx)


class TranslationDataset(Dataset):
    """Dataset for translation task."""

    def __init__(self, df, src_vocab, tgt_vocab):
        self.df = df
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        src = self.src_vocab.encode(row['indonesian'])
        tgt = [self.tgt_vocab.word2idx[SOS_TOKEN]] + \
              self.tgt_vocab.encode(row['papua_kokas']) + \
              [self.tgt_vocab.word2idx[EOS_TOKEN]]
        return torch.tensor(src), torch.tensor(tgt)


def collate_fn(batch):
    """Collate function for DataLoader with padding."""
    src_batch, tgt_batch = zip(*batch)
    src_padded = pad_sequence(src_batch, batch_first=True, padding_value=0)
    tgt_padded = pad_sequence(tgt_batch, batch_first=True, padding_value=0)
    return src_padded, tgt_padded


class Encoder(nn.Module):
    """Bidirectional LSTM Encoder."""

    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, dropout):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim, num_layers,
            batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        # Project bidirectional hidden states to decoder hidden size
        self.fc_hidden = nn.Linear(hidden_dim * 2, hidden_dim)
        self.fc_cell = nn.Linear(hidden_dim * 2, hidden_dim)

    def forward(self, src):
        embedded = self.dropout(self.embedding(src))
        outputs, (hidden, cell) = self.lstm(embedded)

        # Concatenate forward and backward hidden states
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        cell = torch.cat((cell[-2], cell[-1]), dim=1)

        hidden = torch.tanh(self.fc_hidden(hidden))
        cell = torch.tanh(self.fc_cell(cell))

        return outputs, hidden, cell


class Attention(nn.Module):
    """Bahdanau (Additive) Attention."""

    def __init__(self, hidden_dim):
        super().__init__()
        self.attn = nn.Linear(hidden_dim * 3, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, hidden, encoder_outputs, mask):
        batch_size = encoder_outputs.shape[0]
        src_len = encoder_outputs.shape[1]

        # Repeat hidden state for each source position
        hidden = hidden.unsqueeze(1).repeat(1, src_len, 1)

        # Calculate attention energies
        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)

        # Mask padding tokens
        attention = attention.masked_fill(mask == 0, -1e10)

        return torch.softmax(attention, dim=1)


class Decoder(nn.Module):
    """LSTM Decoder with Attention."""

    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, dropout):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.attention = Attention(hidden_dim)
        self.lstm = nn.LSTM(
            embed_dim + hidden_dim * 2, hidden_dim, 1,
            batch_first=True
        )
        self.fc_out = nn.Linear(hidden_dim * 3 + embed_dim, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input, hidden, cell, encoder_outputs, mask):
        input = input.unsqueeze(1)
        embedded = self.dropout(self.embedding(input))

        # Calculate attention weights
        attn_weights = self.attention(hidden, encoder_outputs, mask)
        attn_weights = attn_weights.unsqueeze(1)

        # Apply attention to encoder outputs
        weighted = torch.bmm(attn_weights, encoder_outputs)

        # Concatenate embedded input and weighted context
        lstm_input = torch.cat((embedded, weighted), dim=2)

        output, (hidden, cell) = self.lstm(lstm_input, (hidden.unsqueeze(0), cell.unsqueeze(0)))

        hidden = hidden.squeeze(0)
        cell = cell.squeeze(0)

        # Predict next token
        prediction = self.fc_out(torch.cat((output.squeeze(1), weighted.squeeze(1), embedded.squeeze(1)), dim=1))

        return prediction, hidden, cell, attn_weights.squeeze(1)


class Seq2Seq(nn.Module):
    """Full Seq2Seq model with Attention."""

    def __init__(self, encoder, decoder, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

    def create_mask(self, src):
        return (src != 0).to(self.device)

    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        batch_size = src.shape[0]
        tgt_len = tgt.shape[1]
        tgt_vocab_size = self.decoder.vocab_size

        outputs = torch.zeros(batch_size, tgt_len, tgt_vocab_size).to(self.device)

        encoder_outputs, hidden, cell = self.encoder(src)
        mask = self.create_mask(src)

        # First input is SOS token
        input = tgt[:, 0]

        for t in range(1, tgt_len):
            output, hidden, cell, _ = self.decoder(input, hidden, cell, encoder_outputs, mask)
            outputs[:, t] = output

            # Teacher forcing
            teacher_force = random.random() < teacher_forcing_ratio
            top1 = output.argmax(1)
            input = tgt[:, t] if teacher_force else top1

        return outputs

    def translate(self, src, max_len=50, sos_idx=2, eos_idx=3):
        """Translate a single sentence."""
        self.eval()
        with torch.no_grad():
            encoder_outputs, hidden, cell = self.encoder(src)
            mask = self.create_mask(src)

            input = torch.tensor([sos_idx]).to(self.device)
            outputs = []

            for _ in range(max_len):
                output, hidden, cell, _ = self.decoder(input, hidden, cell, encoder_outputs, mask)
                top1 = output.argmax(1)

                if top1.item() == eos_idx:
                    break

                outputs.append(top1.item())
                input = top1

        return outputs


def train_epoch(model, dataloader, optimizer, criterion, device, clip=1.0):
    """Train for one epoch."""
    model.train()
    total_loss = 0

    for src, tgt in dataloader:
        src, tgt = src.to(device), tgt.to(device)

        optimizer.zero_grad()
        output = model(src, tgt)

        # Reshape for loss calculation (ignore SOS token)
        output = output[:, 1:].reshape(-1, output.shape[-1])
        tgt = tgt[:, 1:].reshape(-1)

        loss = criterion(output, tgt)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)


def evaluate_model(model, dataloader, criterion, device):
    """Evaluate on validation set."""
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for src, tgt in dataloader:
            src, tgt = src.to(device), tgt.to(device)
            output = model(src, tgt, teacher_forcing_ratio=0)

            output = output[:, 1:].reshape(-1, output.shape[-1])
            tgt = tgt[:, 1:].reshape(-1)

            loss = criterion(output, tgt)
            total_loss += loss.item()

    return total_loss / len(dataloader)


def translate_dataset(model, df, src_vocab, tgt_vocab, device):
    """Translate entire dataset and return predictions."""
    model.eval()
    predictions = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Translating"):
        src = torch.tensor([src_vocab.encode(row['indonesian'])]).to(device)
        output_indices = model.translate(src, sos_idx=tgt_vocab.word2idx[SOS_TOKEN],
                                          eos_idx=tgt_vocab.word2idx[EOS_TOKEN])
        prediction = tgt_vocab.decode(output_indices)
        predictions.append(prediction)

    return predictions


def compute_metrics(predictions, references):
    """Compute BLEU, chrF, and TER."""
    bleu = evaluate.load("bleu")
    chrf = evaluate.load("chrf")
    ter = evaluate.load("ter")

    formatted_refs = [[r.lower().strip()] for r in references]
    formatted_preds = [p.lower().strip() for p in predictions]

    bleu_score = bleu.compute(predictions=formatted_preds, references=formatted_refs)
    chrf_score = chrf.compute(predictions=formatted_preds, references=formatted_refs)
    ter_score = ter.compute(predictions=formatted_preds, references=formatted_refs)

    return {
        'bleu': bleu_score['bleu'] * 100,
        'chrf': chrf_score['score'],
        'ter': ter_score['score']
    }


def main():
    print("=" * 60)
    print("LSTM SEQ2SEQ WITH ATTENTION BASELINE")
    print("=" * 60)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nUsing device: {device}")

    # Load data
    print("\n1. Loading data...")
    train_df = pd.read_csv(TRAIN_PATH)
    val_df = pd.read_csv(VAL_PATH)
    test_df = pd.read_csv(TEST_PATH)
    print(f"   Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    # Build vocabularies
    print("\n2. Building vocabularies...")
    src_vocab = Vocabulary(min_freq=MIN_FREQ)
    tgt_vocab = Vocabulary(min_freq=MIN_FREQ)
    src_vocab.build(train_df['indonesian'].tolist())
    tgt_vocab.build(train_df['papua_kokas'].tolist())
    print(f"   Source vocab size: {len(src_vocab)}")
    print(f"   Target vocab size: {len(tgt_vocab)}")

    # Create datasets and dataloaders
    train_dataset = TranslationDataset(train_df, src_vocab, tgt_vocab)
    val_dataset = TranslationDataset(val_df, src_vocab, tgt_vocab)
    test_dataset = TranslationDataset(test_df, src_vocab, tgt_vocab)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)

    # Initialize model
    print("\n3. Initializing model...")
    encoder = Encoder(len(src_vocab), EMBEDDING_DIM, HIDDEN_DIM, NUM_LAYERS, DROPOUT)
    decoder = Decoder(len(tgt_vocab), EMBEDDING_DIM, HIDDEN_DIM, NUM_LAYERS, DROPOUT)
    model = Seq2Seq(encoder, decoder, device).to(device)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"   Total parameters: {total_params:,}")
    print(f"   Trainable parameters: {trainable_params:,}")

    # Optimizer and loss
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding

    # Training
    print(f"\n4. Training for max {NUM_EPOCHS} epochs (early stopping patience: {PATIENCE})...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    best_val_loss = float('inf')
    patience_counter = 0
    train_losses = []
    val_losses = []

    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss = evaluate_model(model, val_loader, criterion, device)

        train_losses.append(train_loss)
        val_losses.append(val_loss)

        print(f"   Epoch {epoch+1:3d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'best_model.pt'))
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f"\n   Early stopping at epoch {epoch+1}")
                break

    # Load best model
    print("\n5. Loading best model and evaluating on test set...")
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'best_model.pt')))

    # Translate test set
    predictions = translate_dataset(model, test_df, src_vocab, tgt_vocab, device)
    references = test_df['papua_kokas'].tolist()

    # Compute metrics
    scores = compute_metrics(predictions, references)

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS: LSTM SEQ2SEQ WITH ATTENTION")
    print("=" * 60)
    print(f"BLEU:   {scores['bleu']:.2f}")
    print(f"chrF++: {scores['chrf']:.2f}")
    print(f"TER:    {scores['ter']:.2f}")
    print("=" * 60)

    # Save results
    results = {
        'model': 'LSTM Seq2Seq',
        'architecture': 'Bidirectional LSTM + Bahdanau Attention',
        'bleu': round(scores['bleu'], 2),
        'chrf': round(scores['chrf'], 2),
        'ter': round(scores['ter'], 2),
        'hyperparameters': {
            'embedding_dim': EMBEDDING_DIM,
            'hidden_dim': HIDDEN_DIM,
            'num_layers': NUM_LAYERS,
            'dropout': DROPOUT,
            'batch_size': BATCH_SIZE,
            'learning_rate': LEARNING_RATE,
            'total_params': total_params
        },
        'training': {
            'epochs_run': len(train_losses),
            'best_val_loss': best_val_loss,
            'final_train_loss': train_losses[-1],
            'final_val_loss': val_losses[-1]
        },
        'vocabulary': {
            'source_size': len(src_vocab),
            'target_size': len(tgt_vocab)
        }
    }

    with open(os.path.join(OUTPUT_DIR, 'lstm_seq2seq_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {OUTPUT_DIR}/lstm_seq2seq_results.json")

    # Show sample translations
    print("\n" + "=" * 60)
    print("SAMPLE TRANSLATIONS")
    print("=" * 60)
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
