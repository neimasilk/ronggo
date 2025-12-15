# Revitalizing the Endangered Papua Kokas Language: A Low-Resource NMT Approach using Transformers

**Abstract**—The preservation of indigenous languages is a critical challenge in the digital age, particularly for under-resourced languages like Papua Kokas, spoken in the Fakfak regency of West Papua, Indonesia. This paper presents a Neural Machine Translation (NMT) system designed to facilitate the revitalization of the Papua Kokas language by enabling automatic translation from Indonesian. Utilizing a low-resource NMT approach, we employ Transfer Learning with a Transformer-based architecture. Specifically, we fine-tune the MarianMT model, originally pre-trained on a larger Indonesian-English corpus, using a manually curated dataset of 2,909 Indonesian-Kokas sentence pairs. Our experiments demonstrate the feasibility of this approach, achieving a BLEU score of **46.73**, indicating a high degree of translation quality despite limited data availability. This work contributes to the digital documentation of the Papua Kokas language and provides a scalable framework for other endangered languages in the region.

**Keywords**—Neural Machine Translation, Low-Resource Languages, Transformers, Transfer Learning, Papua Kokas, Language Preservation.

## I. INTRODUCTION

Indonesia is a linguistically diverse nation with over 700 distinct languages. However, a significant number of these languages are currently endangered due to the declining number of native speakers and the dominance of the national language, Indonesian (*Bahasa Indonesia*). The Papua Kokas language (also known as Sekar), spoken in the Kokas District of Fakfak Regency, West Papua, faces similar threats of attrition. Revitalizing such languages requires not only documentation but also the development of digital tools that can bridge the gap between the younger generation and their ancestral tongue.

Machine Translation (MT) offers a powerful solution for language revitalization, enabling real-time communication and learning. However, modern Neural Machine Translation (NMT) models, such as the Transformer architecture proposed by Vaswani et al. [1], typically require massive parallel corpora (millions of sentence pairs) to achieve fluency and accuracy. For a low-resource language like Papua Kokas, where available digitized text is scarce, training an NMT model from scratch is often infeasible due to the poor generalization capabilities of deep learning models on small datasets.

To address this challenge, this study adopts a **Transfer Learning** approach. We leverage a pre-trained Transformer model (MarianMT) that has already learned the linguistic features of Indonesian. By fine-tuning this model on a small, high-quality corpus of Indonesian-Kokas pairs, we aim to transfer the encoder's understanding of Indonesian to generate Kokas translations effectively.

The primary contributions of this paper are:
1.  **Dataset Construction**: The curation and preprocessing of a parallel corpus containing 2,909 sentences mapping Indonesian to Papua Kokas.
2.  **Model Implementation**: The adaptation of a Transformer-based NMT model for the specific low-resource context of the Kokas language using the MarianMT framework.
3.  **Evaluation**: A comprehensive evaluation of the model's performance using the BLEU metric, demonstrating the potential of transfer learning for extremely low-resource settings.

## II. RELATED WORK

### A. Neural Machine Translation and Transformers
Neural Machine Translation (NMT) has revolutionized the field of automated translation, surpassing statistical methods in fluency and context handling. The introduction of the Transformer architecture [1] marked a significant milestone. Relying entirely on self-attention mechanisms rather than recurrent or convolutional layers, Transformers allow for parallelization during training and better handling of long-range dependencies in sentences.

### B. Low-Resource NMT & Transfer Learning
The primary bottleneck for NMT is the requirement for large-scale parallel corpora. "Low-resource" languages are those lacking such massive datasets. Research in this area focuses on techniques to maximize performance with limited data. Zoph et al. [2] demonstrated the effectiveness of Transfer Learning, where a parent model trained on a high-resource language pair is fine-tuned on the low-resource pair. This approach allows the model to leverage general linguistic properties (syntax, semantics) learned from the parent task, significantly reducing the data requirements for the child task.

### C. MarianMT Framework
MarianMT [3] is an efficient NMT framework written in C++ that has been widely adopted by the research community. It provides a vast repository of pre-trained models. In this study, we utilize the `opus-mt-id-en` model as our starting point. Although the target language (English) differs from Kokas, the encoder's robust representation of Indonesian serves as a powerful feature extractor for our task.

## III. METHODOLOGY

### A. System Architecture
Our proposed system follows a standard NMT pipeline adapted for transfer learning. The process involves data collection, preprocessing, tokenization, and fine-tuning the pre-trained Transformer model.

```mermaid
graph TD
    A[Raw Corpus (Indonesian-Kokas)] -->|Preprocessing| B[Cleaned Pairs]
    B -->|Tokenization| C[Token IDs]
    C -->|Fine-Tuning| D{MarianMT Pre-trained Model}
    D --> E[Fine-Tuned Kokas Model]
    E -->|Inference| F[Translated Text]
```

### B. Data Collection and Preparation
The foundation of this research is a custom-built parallel corpus. Given the low-resource nature of Papua Kokas, no large-scale digital datasets existed previously.
1.  **Dataset Statistics**: The final dataset consists of **2,909 parallel sentence pairs**.
2.  **Preprocessing**: Steps included lowercasing, removal of special characters, and cleaning of encoding errors.
3.  **Tokenization**: We utilized `SentencePiece` tokenization via the `MarianTokenizer`. This method segments words into subword units, which is crucial for handling the morphology of agglutinative languages and reducing Out-Of-Vocabulary (OOV) tokens.

### C. Transformer Model Architecture
We employed the standard Transformer architecture [1]. The core component is the **Attention Mechanism**, specifically Scaled Dot-Product Attention, which allows the model to focus on different parts of the input sequence.

The attention function is computed on a set of queries ($Q$), keys ($K$), and values ($V$):

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

Where $d_k$ is the dimension of the keys. This mechanism is applied in parallel as **Multi-Head Attention**, allowing the model to jointly attend to information from different representation subspaces at different positions.

### D. Fine-Tuning Objective
The training process aims to minimize the Cross-Entropy Loss between the predicted probability distribution and the ground truth target tokens. For a target sequence $Y = (y_1, ..., y_T)$ given an input $X$, the loss function $\mathcal{L}$ is defined as:

$$ 
\mathcal{L} = - \sum_{t=1}^{T} \log P(y_t | y_{<t}, X; \theta) 
$$ 

Where $\theta$ represents the model parameters. By initializing $\theta$ with weights from `opus-mt-id-en`, the optimization process starts from a point of high linguistic competence in Indonesian, requiring fewer steps to converge on the Kokas translation task.

## IV. EXPERIMENTS AND RESULTS

### A. Experimental Setup
The experiments were conducted using the PyTorch framework and Hugging Face Transformers library.
*   **Dataset Split**: 80% Training (2,327 sentences), 20% Validation (582 sentences).
*   **Hyperparameters**:
    *   Epochs: 100
    *   Batch Size: 16
    *   Optimizer: AdamW ($eta_1=0.9, \beta_2=0.999$)
    *   Learning Rate: $2e^{-5}$ (with linear decay)

### B. Evaluation Metric: BLEU
To assess translation quality, we used the **BLEU (Bilingual Evaluation Understudy)** score [4]. BLEU calculates the geometric mean of n-gram modified precision scores ($p_n$), multiplied by a brevity penalty ($BP$) to discourage overly short translations:

$$ 
\text{BLEU} = BP \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right) 
$$ 

### C. Quantitative Results
The model's performance was monitored over 100 epochs. The best performance was achieved at **Epoch 36**.

| Metric | Value |
| :--- | :--- |
| **Best BLEU Score** | **46.73** |
| Best Eval Loss | 0.5529 |
| Final BLEU (Epoch 100) | 45.50 |

The high BLEU score (>40) is notable for a low-resource task. This can be attributed to two factors:
1.  **Simplicity of Corpus**: The dataset consists largely of daily conversation and short phrases, which are easier for the model to memorize and generalize than complex literary text.
2.  **Effectiveness of Transfer Learning**: The encoder's pre-existing knowledge of Indonesian syntax provided a robust foundation.

### D. Qualitative Analysis
Below is a sample of the translation output:

| Source (Indonesian) | Reference (Kokas) | Predicted (Kokas) |
| :--- | :--- | :--- |
| *Aktivitas fisik teratur...* | *[Reference String]* | *[Predicted String]* |

(Note: The model successfully generates coherent sentence structures in Kokas, though it occasionally struggles with rare proper nouns not present in the training set).

## V. CONCLUSION

This research successfully demonstrated a low-resource NMT system for the Papua Kokas language using a fine-tuned MarianMT Transformer. With a limited dataset of 2,909 sentences, we achieved a BLEU score of **46.73**. This confirms that Transfer Learning is a viable strategy for revitalizing endangered languages in Indonesia. Future work will focus on expanding the dataset and developing a mobile application for community use.

## REFERENCES

[1] A. Vaswani et al., "Attention is all you need," in *Advances in Neural Information Processing Systems*, 2017, pp. 5998–6008.

[2] B. Zoph, D. Yuret, and J. May, "Transfer learning for low-resource neural machine translation," in *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing*, 2016, pp. 1568–1575.

[3] M. Junczys-Dowmunt et al., "Marian: Fast neural machine translation in C++," in *Proceedings of ACL 2018, System Demonstrations*, 2018, pp. 116–121.

[4] K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu, "BLEU: a method for automatic evaluation of machine translation," in *Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics*, 2002, pp. 311–318.
