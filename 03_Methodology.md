# 3. Methodology

## 3.1 Data Collection and Preparation
The foundation of this research is a custom-built parallel corpus of Indonesian and Papua Kokas sentences. Given the low-resource nature of Papua Kokas, no large-scale digital datasets existed previously.

### 3.1.1 Dataset Statistics
The final dataset consists of **2,909 parallel sentence pairs**. These pairs cover daily conversation topics, greetings, and common expressions relevant to the speakers in Fakfak, West Papua.

### 3.1.2 Preprocessing
The raw data, collected in spreadsheet formats (`.csv` and `.xlsx`), underwent several preprocessing steps:
1.  **Cleaning**: Removal of duplicate entries and correction of encoding errors.
2.  **Normalization**: Lowercasing and removal of special characters where appropriate to reduce vocabulary size complexity.
3.  **Tokenization**: We utilized the `MarianTokenizer`, which employs SentencePiece tokenization. This method is particularly effective for agglutinative languages or languages with complex morphology, as it breaks words down into subword units, mitigating the "out-of-vocabulary" (OOV) problem.

### 3.1.3 Data Splitting
To ensure robust evaluation, the dataset was split into training and validation sets using a random stratified sampling approach:
-   **Training Set**: 80% (approx. 2,327 sentences)
-   **Validation Set**: 20% (approx. 582 sentences)

## 3.2 Model Architecture
We employed the **Transformer** architecture, specifically the implementation within the MarianMT framework (`Helsinki-NLP/opus-mt-id-en`). The model consists of an Encoder-Decoder structure with attention mechanisms.

### 3.2.1 The Encoder
The encoder processes the input sequence (Indonesian text) $X = (x_1, ..., x_n)$. It uses self-attention layers to understand the context of each word relative to every other word in the sentence, creating a context-rich representation. Since we use a pre-trained model, the encoder already possesses a strong semantic understanding of Indonesian syntax and vocabulary.

### 3.2.2 The Decoder
The decoder generates the target sequence (Papua Kokas text) $Y = (y_1, ..., y_m)$. It uses masked self-attention (to prevent seeing future tokens) and cross-attention (to focus on relevant parts of the encoder output). During fine-tuning, the decoder learns the mapping from the Indonesian representations to the Kokas vocabulary and sentence structure.

### 3.2.3 Fine-Tuning Strategy
Instead of training from scratch, which would require millions of sentences, we fine-tune all parameters of the pre-trained model. The objective is to minimize the Cross-Entropy Loss between the predicted token distribution and the actual Kokas tokens.
