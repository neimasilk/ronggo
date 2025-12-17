# Revitalizing the Endangered Papua Kokas Language: A Low-Resource NMT Approach using Transformers

## 1. Introduction
- **Background**: Language endangerment in Indonesia/Papua. The need for preservation.
- **Problem**: Low-resource setting (scarcity of parallel corpora for Kokas-Indonesia).
- **Solution**: Neural Machine Translation (NMT) using Transfer Learning (MarianMT/Transformers).
- **Contributions**:
    - Creation of a parallel corpus (Indonesia-Kokas).
    - Fine-tuning a Transformer model.
    - Evaluation using BLEU scores.

## 2. Related Work
- NMT for Low-Resource Languages.
- Transfer Learning in NMT.
- Previous studies on local Indonesian languages (if any).

## 3. Methodology
### 3.1 Data Collection and Preprocessing
- **Source**: Primary data collection (fieldwork/interviews) and existing texts.
- **Statistics**: 2,909 sentence pairs.
- **Preprocessing**: Tokenization, cleaning, train/test split (80/20).

### 3.2 Model Architecture
- **Base Model**: MarianMT (Helsinki-NLP/opus-mt-id-en) - Pre-trained on Indonesian-English.
- **Architecture**: Transformer (Encoder-Decoder with Attention).
- **Fine-tuning Strategy**: Adaptation to the Kokas target language.

### 3.3 Experimental Setup
- **Framework**: Hugging Face Transformers, PyTorch.
- **Hyperparameters**:
    - Epochs: 100
    - Batch Size: 16
    - Optimizer: AdamW
    - Learning Rate scheduler (if applicable).

## 4. Results and Discussion
- **Quantitative Results**:
    - Training Loss vs Validation Loss curves.
    - BLEU Scores over epochs.
    - Final BLEU Score achieved.
- **Qualitative Analysis**:
    - Examples of good translations.
    - Examples of errors (rare words, grammatical structure mismatches).

## 5. Conclusion and Future Work
- **Summary**: Successfully built a prototype NMT for Kokas.
- **Future Work**: Increasing dataset size, exploring other architectures, developing a mobile app.

## References
- (To be filled with standard NMT citations: Vaswani et al., etc.)
