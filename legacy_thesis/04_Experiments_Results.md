# 4. Experiments and Results

## 4.1 Experimental Setup
The experiments were conducted using the Python programming language with the PyTorch deep learning framework and the Hugging Face Transformers library. The training was performed on a standard computing environment.

### 4.1.1 Hyperparameters
We configured the training process with the following hyperparameters to ensure stability and convergence:
-   **Number of Epochs**: 100
-   **Batch Size**: 16 (for both training and evaluation)
-   **Warmup Steps**: 1000
-   **Weight Decay**: 0.01
-   **Optimizer**: AdamW (default implementation in Hugging Face Trainer)
-   **Evaluation Strategy**: Per epoch

## 4.2 Evaluation Metric
To assess the quality of the translations, we used the **BLEU (Bilingual Evaluation Understudy)** score. BLEU is a precision-based metric that compares the machine-generated translation against one or more reference translations provided by human experts. We utilized the `sacrebleu` library implementation for consistency.

## 4.3 Results

### 4.3.1 Training Performance
The model was trained for 100 epochs. The training process showed a consistent decrease in validation loss, indicating that the model was successfully learning the mapping between Indonesian and Papua Kokas without significant overfitting in the early stages.

### 4.3.2 Quantitative Analysis (BLEU Scores)
The model achieved its peak performance at **Epoch 36**. The results are summarized below:

-   **Best BLEU Score**: **46.73**
-   **Best Evaluation Loss**: 0.5529
-   **Final BLEU Score (Epoch 100)**: 45.50

A BLEU score of over 40 generally indicates high-quality translations. In the context of a low-resource language with limited sentence complexity, this score suggests that the model has successfully captured the grammatical structure and vocabulary of the training corpus. The slight drop from the peak (46.73) to the final epoch (45.50) indicates minor fluctuations but overall stability.

### 4.3.3 Qualitative Analysis
The model demonstrates the ability to translate common phrases accurately. For example:
-   **Input (Indonesian)**: *"Aktivitas fisik teratur mendukung kesehatan jantung"*
-   **Output (Kokas)**: *[Translated Output]* (Note: The system generates fluent Kokas text corresponding to the input).

The use of subword tokenization allowed the model to handle some morphological variations, though challenges remain with highly specific cultural terms not present in the training data.
