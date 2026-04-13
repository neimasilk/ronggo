# **Revitalizing the Endangered Papua Kokas Language: A Low-Resource NMT Approach using Transformers**

**Authors:**

* **Nira Radita** (1) \- niraradita@ubhinus.ac.id  
* **Mukhlis Amien** (2) \- amien@ubhinus.ac.id  
* **Ronggo Haikal** (3) \- ronggohaikal05@gmail.com

*(1)(2)(3) Universitas Bhinneka Nusantara, Malang, Indonesia*

## **Abstract**

**Background:** Many indigenous languages in eastern Indonesia, including the Papua Kokas language, are endangered due to limited documentation and the dominance of national and global languages. The scarcity of parallel corpora makes the development of automatic translation systems for such languages particularly challenging, requiring approaches that can operate effectively under low-resource conditions.

**Objective:** This study aims to develop and evaluate a low-resource Neural Machine Translation (NMT) system to support the revitalization of the Papua Kokas language by enabling automatic translation from Indonesian. Additionally, this study compares the performance of different translation approaches, including traditional word-based methods, recurrent neural networks, and Transformer-based architectures.

**Methods:** Three translation approaches were implemented and compared: (1) a word-based dictionary baseline, (2) an LSTM-based sequence-to-sequence model with attention, and (3) a Transformer-based NMT model using the NLLB-200 (No Language Left Behind) framework. All models were trained and evaluated on a manually collected parallel corpus consisting of 4,057 Indonesian–Papua Kokas sentence pairs obtained through interviews with native speakers. Translation quality was evaluated using multiple metrics including BLEU, chrF++, and TER. The best-performing model was deployed in a web-based application to support real-time translation.

**Results:** Experimental results demonstrate that the Transformer-based NLLB-200 model significantly outperforms other approaches, achieving a BLEU score of 59.54, chrF++ of 79.45, and TER of 27.70. In comparison, the LSTM sequence-to-sequence model achieved a BLEU of 30.74, while the word-based baseline achieved only 19.23. These results confirm the superiority of the self-attention mechanism in capturing linguistic patterns for low-resource translation tasks.

**Conclusion:** The findings demonstrate that a Transformer-based NMT approach, particularly using multilingual pre-trained models like NLLB-200, is significantly more effective than traditional and RNN-based methods for low-resource language translation. The high chrF++ score indicates strong morphological accuracy, which is essential for languages with unique grammatical structures like Papua Kokas. This approach not only supports practical communication needs but also contributes to digital language preservation efforts.

**Keywords:** Low-resource NMT, Transformers, NLLB-200, Papua Kokas language, language revitalization, machine translation

## **Introduction**

Indonesia is one of the most linguistically diverse countries in the world, with more than 700 regional languages distributed across its archipelago \[1\]. A significant proportion of these languages are spoken in eastern Indonesia, particularly in Papua, where many local languages are currently classified as endangered \[2\]. One such language is Papua Kokas, which is increasingly marginalized due to limited intergenerational transmission, insufficient documentation, and the dominance of Indonesian as the national language. Without adequate technological support and digital representation, languages like Papua Kokas face a high risk of extinction.

Automatic Machine Translation (MT) has emerged as an important technological tool for improving access to information and facilitating communication across language barriers \[3\]–\[5\]. In recent years, Neural Machine Translation (NMT) has demonstrated superior performance compared to traditional rule-based and statistical approaches, particularly through the adoption of Transformer architectures that rely on self-attention mechanisms rather than recurrent structures \[6\], \[7\]. Transformers have achieved state-of-the-art results in many high-resource language pairs and are increasingly explored for low-resource scenarios \[8\].

Despite these advances, most existing NMT systems are developed for widely spoken languages with abundant parallel corpora. Low-resource languages, such as Papua Kokas, present unique challenges due to the scarcity of training data and limited prior research. Previous studies on Indonesian regional languages have mainly focused on languages with relatively larger corpora or have relied on recurrent neural network architectures, pivot languages, or rule-based methods. Research that specifically addresses Transformer-based NMT for endangered Papuan languages remains very limited.

This study addresses this research gap by proposing a low-resource Transformer-based NMT approach for translating Indonesian into Papua Kokas. Using a manually collected parallel corpus of 4,057 sentence pairs, this research investigates whether a fine-tuned Transformer model implemented with the NLLB-200 (No Language Left Behind) framework can produce reliable translations despite data constraints. To provide comprehensive evaluation, this study compares the Transformer approach against traditional word-based translation and LSTM-based sequence-to-sequence models. Translation quality is evaluated using multiple metrics including BLEU, chrF++, and TER, and the trained model is deployed in a web-based application to demonstrate practical usability.

This study makes several distinct and original contributions to the field of low-resource Neural Machine Translation. This work represents one of the first Transformer-based NMT studies targeting the endangered Papua Kokas language, for which no publicly available translation system has previously been reported. Unlike prior studies that rely on pivot languages, larger regional corpora, or recurrent architectures, this research demonstrates that a direct Indonesian–Papua Kokas translation model can be effectively trained using a limited parallel dataset. The study provides a systematic comparison between different translation paradigms—word-based, RNN-based, and Transformer-based—offering empirical evidence for the superiority of self-attention mechanisms in low-resource settings. Furthermore, this research analyzes the unique linguistic characteristics of the Papua Kokas language and discusses how Transformer architectures accommodate these features through subword tokenization and multilingual transfer learning. By deploying the trained model into a web-based translation application, this research bridges the gap between theoretical NMT development and practical language revitalization, highlighting how modern Transformer architectures can support endangered language preservation through real-world digital tools.

## **Literature Review**

Neural Machine Translation (NMT) has become the dominant paradigm in automatic translation due to its ability to model contextual dependencies more effectively than rule-based and statistical approaches \[9\]. Early NMT systems predominantly relied on recurrent neural networks (RNNs) with encoder–decoder architectures, which demonstrated improvements in translation fluency but suffered from limitations such as long-range dependency degradation and sequential computation constraints \[10\]. These issues are particularly pronounced in low-resource settings, where limited training data restricts model generalization.

The introduction of the Transformer architecture marked a significant shift in NMT research. By replacing recurrence with self-attention mechanisms, Transformers enable parallel computation and more effective contextual representation. Studies have shown that Transformer-based models outperform RNN-based architectures in many language pairs, especially when sufficient training data are available \[11\]. However, their application to low-resource and endangered languages remains an active research challenge, as Transformers typically benefit from large-scale corpora.

Several studies have explored NMT for Indonesian and regional languages. Research on Indonesian–Lampung and Indonesian–Sundanese translation has demonstrated that NMT can outperform traditional methods, but these studies often rely on RNN or LSTM architectures and comparatively larger datasets \[12\], \[13\]. While attention mechanisms have been incorporated to improve translation accuracy, such approaches still face difficulties handling out-of-vocabulary terms and contextual ambiguity when training data are scarce. These limitations motivate the exploration of Transformer-based methods that inherently model global context.

More recent works have applied Transformer architectures to Indonesian-language tasks such as text summarization, offensive language detection, and translation between regional languages \[14\]. Some studies employ pivot languages as intermediaries to improve translation quality between two low-resource languages \[15\]. Although pivot-based approaches can enhance accuracy, they introduce additional complexity and require supplementary corpora, which may not be feasible for endangered languages with minimal documentation.

Research on Papuan languages remains extremely limited in the context of machine translation. Existing linguistic and documentation-focused studies emphasize the urgency of preserving Papuan languages but rarely integrate computational approaches. To date, very few studies have reported the application of Transformer-based NMT to Papuan regional languages, and none have systematically evaluated translation performance using standardized metrics such as BLEU in a low-resource Indonesian-to-Papuan scenario.

Evaluation of NMT systems is commonly conducted using automatic metrics, with BLEU being the most widely adopted. BLEU enables quantitative comparison between machine-generated translations and reference sentences and is frequently used to analyze model convergence across training epochs \[16\]. While BLEU does not fully capture semantic adequacy or linguistic naturalness, it remains a practical benchmark for low-resource NMT studies, particularly when human evaluation is difficult to conduct \[17\].

Based on the existing literature, two key gaps can be identified. First, there is a lack of empirical studies applying Transformer-based NMT directly to endangered Papuan languages without relying on pivot languages. Second, limited attention has been given to analyzing training behavior and performance trends of Transformer models under severely constrained data conditions. This study addresses these gaps by implementing and evaluating a low-resource Transformer-based NMT model for Indonesian–Papua Kokas translation, contributing both empirical evidence and practical insights to the field of endangered language technology.

## **Methods**

### **Research Design**

This study adopts a quantitative experimental research design to evaluate the effectiveness of a Transformer-based Neural Machine Translation (NMT) model in a low-resource language setting. The experiment focuses on automatic translation from Indonesian to the Papua Kokas language using a parallel corpus and objective evaluation metrics. The overall research workflow consists of data collection, preprocessing, model fine-tuning and deployment, as illustrated in Fig. 1.

**Fig. 1: Research Design Flowchart**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Data Collection │───▶│  Preprocessing   │───▶│ Dataset Split   │
│ (Interviews)    │    │ (Cleaning, Norm) │    │ (80/10/10)      │
└─────────────────┘    └──────────────────┘    └────────┬────────┘
                                                        │
                       ┌────────────────────────────────┼────────────────────────────────┐
                       │                                │                                │
                       ▼                                ▼                                ▼
              ┌────────────────┐              ┌────────────────┐              ┌────────────────┐
              │ Word Baseline  │              │ LSTM Seq2Seq   │              │ NLLB-200       │
              │ (Dictionary)   │              │ (Train)        │              │ (Fine-tune)    │
              └───────┬────────┘              └───────┬────────┘              └───────┬────────┘
                      │                               │                               │
                      └───────────────────────────────┼───────────────────────────────┘
                                                      ▼
                                            ┌────────────────┐
                                            │   Evaluation   │
                                            │ (BLEU,chrF,TER)│
                                            └───────┬────────┘
                                                    ▼
                                            ┌────────────────┐
                                            │   Deployment   │
                                            │ (Web App)      │
                                            └────────────────┘
```

*Fig. 1 illustrates the research methodology, showing the flow from data collection through native speaker interviews, preprocessing and dataset splitting, parallel training of three translation approaches (Word Baseline, LSTM Seq2Seq, and NLLB-200 Transformer), unified evaluation using multiple metrics, and deployment in a web application.*

### **Dataset Collection**

The dataset used in this study consists of 4,057 parallel sentence pairs in Indonesian and Papua Kokas. The data were manually collected through interviews with native speakers in the Kokas region, Papua, to ensure linguistic authenticity and contextual relevance. The sentences primarily represent daily conversational expressions, making the dataset suitable for practical translation tasks. The dataset was split into training, validation, and test sets using a strict splitting methodology based on unique Indonesian sentences to prevent data leakage between splits.

**Table 1: Dataset Statistics**

| Parameter | Value |
| :---- | :---- |
| Source Language | Indonesian |
| Target Language | Papua Kokas |
| Total Sentence Pairs | 4,057 |
| Training Split (80%) | 3,239 |
| Validation Split (10%) | 407 |
| Test Split (10%) | 410 |
| Source Vocabulary Size | 1,784 words |
| Target Vocabulary Size | 2,400 words |
| Format | Parallel CSV |

Due to ethical considerations and the protection of indigenous language data, the corpus is not publicly released. However, the data structure and preprocessing steps are fully described to support reproducibility.

### **Data Preprocessing**

Prior to model training, the parallel corpus underwent a series of preprocessing steps to ensure data consistency and compatibility with the Neural Machine Translation framework. The dataset was divided into training, validation, and test sets using an 80:10:10 ratio with strict splitting based on unique source sentences to prevent data leakage and enable objective performance evaluation.

Tokenization for the Transformer model was performed using the SentencePiece tokenizer associated with the NLLB-200 model. This tokenizer applies a subword-based segmentation strategy using Byte Pair Encoding (BPE), enabling the model to effectively handle rare words and morphological variations commonly found in low-resource languages. Subword tokenization is particularly beneficial for the Papua Kokas language, which exhibits productive morphological patterns such as verbal prefixes (e.g., "e-" prefix indicating first person). By decomposing words into smaller meaningful units, the tokenizer reduces the out-of-vocabulary problem and captures morphological regularities.

Several normalization procedures were applied during preprocessing. Case folding was used to convert all text to lowercase, reducing vocabulary size and improving token consistency. Text cleaning was conducted by removing non-standard punctuation marks and excessive whitespace that could introduce noise into the training process.

After tokenization, the text sequences were encoded into numerical representations compatible with PyTorch tensors. Padding and truncation were applied with a maximum sequence length of 128 tokens to produce uniform sequence lengths across batches, which is essential for efficient batch processing and stable model training.

### **Model Configuration**

This study compares three translation approaches to provide comprehensive evaluation:

**Word-based Dictionary Baseline.** A simple word-to-word translation dictionary was constructed from the training data. For each Indonesian word, the most frequently co-occurring Papua Kokas word was selected as the translation. During inference, each word in the input sentence is translated independently using the dictionary, with out-of-vocabulary words copied as-is. This baseline represents the simplest possible translation approach without any contextual understanding.

**LSTM Sequence-to-Sequence with Attention.** A bidirectional LSTM encoder-decoder model with Bahdanau attention was implemented as a neural baseline representing the pre-Transformer era of NMT. The model uses 256-dimensional word embeddings, 512-dimensional hidden states, and 2 layers with dropout of 0.3. Training was conducted using Adam optimizer with learning rate 0.001 and early stopping based on validation loss.

**NLLB-200 Transformer.** The primary translation system is based on the NLLB-200 (No Language Left Behind) architecture, a state-of-the-art multilingual Transformer model developed by Meta AI for low-resource language translation \[24\]. We fine-tuned the `facebook/nllb-200-distilled-600M` pre-trained model, which contains 600 million parameters and supports over 200 languages. Since Papua Kokas is not among the pre-trained languages, we employed a language transfer technique by using the Indonesian (`ind_Latn`) encoder and adapting the decoder through fine-tuning on our parallel corpus.

The NLLB-200 architecture leverages self-attention mechanisms and parallel computation to model long-range dependencies without relying on recurrent structures. The encoder processes Indonesian input sentences, while the decoder generates Papua Kokas translations in an autoregressive manner. Both components follow the standard Transformer configuration consisting of multi-head self-attention layers and position-wise feed-forward networks.

**Fig. 2: Model Architecture Comparison**

```
(a) Word Baseline                (b) LSTM Seq2Seq               (c) NLLB-200 Transformer
                                      with Attention
┌─────────────┐                  ┌─────────────┐                ┌─────────────┐
│   Input     │                  │   Input     │                │   Input     │
│ (Indonesian)│                  │ (Indonesian)│                │ (Indonesian)│
└──────┬──────┘                  └──────┬──────┘                └──────┬──────┘
       │                                │                               │
       ▼                                ▼                               ▼
┌─────────────┐                  ┌─────────────┐                ┌─────────────┐
│ Dictionary  │                  │  Embedding  │                │  Subword    │
│   Lookup    │                  │   Layer     │                │ Tokenizer   │
└──────┬──────┘                  └──────┬──────┘                └──────┬──────┘
       │                                │                               │
       │                                ▼                               ▼
       │                         ┌─────────────┐                ┌─────────────┐
       │                         │ Bi-LSTM     │                │  Encoder    │
       │                         │  Encoder    │                │(Self-Attn)  │
       │                         └──────┬──────┘                └──────┬──────┘
       │                                │                               │
       │                                ▼                               ▼
       │                         ┌─────────────┐                ┌─────────────┐
       │                         │  Attention  │                │Cross-Attn   │
       │                         │  Mechanism  │                │  Decoder    │
       │                         └──────┬──────┘                └──────┬──────┘
       │                                │                               │
       │                                ▼                               ▼
       │                         ┌─────────────┐                ┌─────────────┐
       │                         │   LSTM      │                │  Output     │
       │                         │  Decoder    │                │Projection   │
       │                         └──────┬──────┘                └──────┬──────┘
       │                                │                               │
       ▼                                ▼                               ▼
┌─────────────┐                  ┌─────────────┐                ┌─────────────┐
│   Output    │                  │   Output    │                │   Output    │
│(Papua Kokas)│                  │(Papua Kokas)│                │(Papua Kokas)│
└─────────────┘                  └─────────────┘                └─────────────┘
```

*Fig. 2 compares the three translation architectures: (a) Word Baseline performs simple dictionary lookup without contextual understanding; (b) LSTM Seq2Seq uses bidirectional encoding with Bahdanau attention for context-aware translation; (c) NLLB-200 Transformer employs multi-head self-attention in both encoder and decoder, enabling parallel processing and effective capture of long-range dependencies.*

**Table 2: NLLB-200 Training Hyperparameters**

| Hyperparameter | Value |
| :---- | :---- |
| Base Model | facebook/nllb-200-distilled-600M |
| Parameters | 600 Million |
| Optimizer | AdamW |
| Learning Rate | 2 × 10⁻⁵ |
| Batch Size | 16 |
| Epochs | 20 |
| Weight Decay | 0.01 |
| Precision | FP16 (Mixed Precision) |
| Loss Function | Cross-Entropy |

The loss function minimizes the negative log-likelihood of the target tokens given the input and previous tokens:

$$\mathcal{L} = -\sum_{t=1}^{T} \log P(y_t | y_{<t}, x; \theta)$$

where $T$ is the target sequence length, $y_t$ is the target token at position $t$, $y_{<t}$ represents all preceding tokens, $x$ is the source sequence, and $\theta$ denotes the model parameters.

### **Training Configuration**

Model training for the NLLB-200 Transformer was conducted using the Trainer API provided by the Hugging Face Transformers library. The training process was performed over 20 epochs with mixed precision (FP16) training enabled for computational efficiency. Key hyperparameters included a batch size of 16 for both training and evaluation, weight decay of 0.01 for regularization, and the best model checkpoint was selected based on validation BLEU score.

For the LSTM baseline, training was conducted for up to 100 epochs with early stopping (patience of 10 epochs) based on validation loss to prevent overfitting. The model with the lowest validation loss was selected for final evaluation.

Evaluation was performed at the end of each epoch using the validation dataset. Model checkpoints were saved periodically to allow inspection of performance progression and prevent loss of optimal configurations.

### **Evaluation Metrics**

Translation quality was evaluated using three complementary automatic metrics to provide comprehensive assessment:

**BLEU (Bilingual Evaluation Understudy)** measures the similarity between machine-generated translations and reference sentences based on n-gram overlap and includes a brevity penalty to account for length differences \[16\]. The BLEU score is computed as:

$$BLEU = BP \times \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)$$

where $BP = \min(1, e^{1-r/c})$ is the brevity penalty, $p_n$ is the modified n-gram precision, $w_n$ is the weight for each n-gram (typically $1/N$), $r$ is the reference length, and $c$ is the candidate translation length. BLEU scores range from 0 to 100, with higher scores indicating better translation quality.

**chrF++ (Character n-gram F-score)** evaluates translation quality at the character level, making it particularly suitable for morphologically rich languages where word-level metrics may not capture partial matches \[25\]. The chrF++ score is computed as:

$$chrF_{++} = \frac{(1 + \beta^2) \times chrP \times chrR}{\beta^2 \times chrP + chrR}$$

where $chrP$ is the character n-gram precision, $chrR$ is the character n-gram recall, and $\beta$ is typically set to 2 to weight recall higher than precision. This metric is valuable for the Papua Kokas language, which exhibits productive morphological patterns.

**TER (Translation Edit Rate)** measures the number of edits required to transform the machine translation into the reference translation \[26\]. TER is calculated as:

$$TER = \frac{I + D + S + Sh}{R} \times 100$$

where $I$ is the number of insertions, $D$ is deletions, $S$ is substitutions, $Sh$ is shifts (block movements), and $R$ is the number of words in the reference. Unlike BLEU and chrF++, lower TER scores indicate better translation quality, representing fewer post-editing corrections needed.

These three metrics together provide a more complete picture of translation quality: BLEU captures lexical accuracy, chrF++ captures morphological precision, and TER estimates practical usability for post-editing scenarios.

### **System Deployment**

To demonstrate practical applicability, the trained NMT model was deployed in a web-based translation application developed using the Django framework. The application allows users to input Indonesian text and receive Papua Kokas translations in real time. Model inference is handled on the server side, ensuring consistent translation quality and usability in real-world scenarios.

## **Results**

### **Comparison of Translation Approaches**

Table 3 presents the comparative performance of all three translation approaches evaluated on the test set using BLEU, chrF++, and TER metrics. The results clearly demonstrate the superiority of the Transformer-based NLLB-200 model over both traditional and RNN-based approaches.

**Table 3: Comparison of Translation Methods**

| Model | Architecture | BLEU | chrF++ | TER |
| :---- | :---- | :---- | :---- | :---- |
| Word Baseline | Dictionary Lookup | 19.23 | 48.19 | 55.06 |
| LSTM Seq2Seq | Bi-LSTM + Attention | 30.74 | 58.63 | 47.01 |
| **NLLB-200** | **Transformer** | **59.54** | **79.45** | **27.70** |

The NLLB-200 Transformer model achieved the highest performance across all metrics, with a BLEU score of 59.54, chrF++ of 79.45, and TER of 27.70. Compared to the LSTM Seq2Seq baseline, the Transformer model shows a 94% relative improvement in BLEU score (from 30.74 to 59.54). The word-based dictionary baseline achieved the lowest scores, demonstrating the limitations of context-free translation approaches.

**Fig. 3: Performance Comparison Across Models**

```
BLEU Score (Higher is Better)
│
80 ┤
70 ┤
60 ┤                                              ████████
50 ┤                                              ████████  59.54
40 ┤
30 ┤                    ████████                  ████████
20 ┤   ████████         ████████  30.74           ████████
10 ┤   ████████  19.23  ████████                  ████████
 0 ┼───████████─────────████████──────────────────████████───
       Word             LSTM                      NLLB-200
      Baseline         Seq2Seq                  Transformer

chrF++ Score (Higher is Better)          TER Score (Lower is Better)
│                                        │
80 ┤                     ████  79.45     80 ┤
70 ┤                     ████            70 ┤
60 ┤          ████       ████            60 ┤   ████  55.06
50 ┤   ████   ████ 58.63 ████            50 ┤   ████   ████  47.01
40 ┤   ████   ████       ████            40 ┤   ████   ████
   │   48.19                             30 ┤   ████   ████   ████  27.70
30 ┤   ████   ████       ████            20 ┤   ████   ████   ████
 0 ┼───████───████───────████───          0 ┼───████───████───████───
      Word   LSTM      NLLB-200               Word   LSTM   NLLB-200
```

*Fig. 3 visualizes the performance comparison across three models. The NLLB-200 Transformer achieves the highest BLEU (59.54) and chrF++ (79.45) scores, while also obtaining the lowest TER (27.70), indicating superior translation quality across all metrics.*

### **NLLB-200 Training Performance**

The NLLB-200 model was trained for 20 epochs using the Indonesian–Papua Kokas parallel corpus. Table 4 presents selected BLEU scores and evaluation losses across representative epochs to illustrate the progression of translation quality during training.

**Table 4: NLLB-200 Training Progress**

| Epoch | Evaluation Loss | BLEU Score |
| :---- | :---- | :---- |
| 1 | 6.97 | 15.46 |
| 5 | 0.48 | 52.30 |
| 10 | 0.35 | 57.82 |
| 15 | 0.32 | 58.91 |
| 20 | 0.31 | 59.54 |

The BLEU score increased rapidly during the initial epochs, rising from 15.46 at epoch 1 to over 52 by epoch 5, demonstrating effective transfer learning from the multilingual pre-trained model. The model converged around epoch 15-20, with final performance stabilizing at approximately 59.54 BLEU.

**Fig. 4: NLLB-200 Training Progress**

```
BLEU Score
│
60 ┤                              ●────●────●────●  59.54
   │                         ●────┘
55 ┤                    ●────┘
   │               ●────┘
50 ┤          ●────┘
   │
45 ┤
   │
40 ┤
   │
35 ┤
   │
30 ┤
   │
25 ┤
   │
20 ┤     ●
15 ┤●────┘  15.46
   │
10 ┤
 0 ┼────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬
   0    2    4    6    8   10   12   14   16   18   20
                         Epoch

Legend: ● BLEU Score (Validation Set)
```

*Fig. 4 shows the BLEU score progression during NLLB-200 training. The rapid improvement in early epochs (1-5) demonstrates effective transfer learning from the multilingual pre-trained model. The curve plateaus around epoch 15, indicating model convergence at approximately 59.54 BLEU.*

### **Qualitative Translation Results**

In addition to quantitative evaluation, qualitative inspection was conducted to compare the translation outputs across all three approaches. Table 5 presents selected examples of Indonesian input sentences and their corresponding Papua Kokas translations generated by each model.

**Table 5: Comparison of Translation Outputs Across Models**

| Indonesian | Reference | Word Baseline | LSTM Seq2Seq | NLLB-200 |
| :---- | :---- | :---- | :---- | :---- |
| saya akan pergi ke pasar | yai emau eti pasar | yai kesadaran pasar ami | yai emau eti pasar | yai emau eti pasar |
| bagaimana kabarmu | akape o habar | o kusafa kusafa | akape o | akape o habar |
| tolong beri tahu saya | tolong farok ati yai | tolong farok ati yai | tolong farok ati yai | tolong farok ati yai |

The qualitative results demonstrate clear differences between the approaches. The Word Baseline produces grammatically incorrect translations due to lack of context awareness and inability to handle word order differences between the two languages. The LSTM Seq2Seq model generates more reasonable translations but occasionally produces incomplete outputs or unknown tokens, indicating vocabulary limitations inherent in models trained from scratch on small datasets. In contrast, the NLLB-200 Transformer produces the most accurate and fluent translations, correctly handling morphological patterns such as the verbal prefix "e-" (e.g., "emau" for "will") and maintaining proper word order throughout the sentence.

The NLLB-200 model demonstrates particular strength in capturing the morphological patterns unique to Papua Kokas, as evidenced by the high chrF++ score (79.45), which measures character-level accuracy and is particularly indicative of morphological competence.

## **Discussion**

### **Comparative Analysis of Translation Approaches**

The experimental results clearly demonstrate that the Transformer-based NLLB-200 model significantly outperforms both the word-based dictionary baseline and the LSTM sequence-to-sequence model across all evaluation metrics. The NLLB-200 achieved a BLEU score of 59.54, representing a 94% relative improvement over the LSTM model (30.74) and a 210% improvement over the word baseline (19.23).

The word-based dictionary baseline, despite its simplicity, achieved a BLEU score of 19.23, which is higher than expected for such a naive approach. This can be attributed to the relatively fixed word order patterns and high lexical overlap between Indonesian and Papua Kokas in the conversational domain. However, the high TER score (55.06) indicates that substantial post-editing would be required, making this approach impractical for real-world use.

The LSTM Seq2Seq model with attention achieved a BLEU score of 30.74, demonstrating that neural approaches can learn meaningful translation patterns even with limited data. However, the model exhibited signs of overfitting (early stopping triggered at epoch 15) and struggled with out-of-vocabulary words, often producing incomplete translations or unknown tokens. These limitations are consistent with prior research indicating that RNN-based architectures require larger datasets to achieve stable generalization \[10\], \[13\].

The Transformer-based NLLB-200 model's superior performance can be attributed to several factors: (1) the self-attention mechanism's ability to capture long-range dependencies without the sequential processing limitations of RNNs, (2) the benefit of multilingual pre-training on 200+ languages that provides robust cross-lingual representations, and (3) subword tokenization that effectively handles morphological variations and reduces out-of-vocabulary problems.

### **Linguistic Characteristics of Papua Kokas and Transformer Accommodation**

The Papua Kokas language, also known as Sekar language, belongs to the North Bomberai family within the Austronesian language group. This language exhibits several distinctive linguistic characteristics that differentiate it from both Indonesian and other Papuan languages:

**Unique Pronominal System.** Papua Kokas uses distinct pronouns that differ from both standard Indonesian and Papuan Malay varieties. The first-person singular pronoun is "yai" (compared to Indonesian "saya/aku" and Papuan Malay "sa"), while the second-person singular is "o" (compared to Indonesian "kamu" and Papuan Malay "ko"). This distinct pronominal system requires the translation model to learn entirely new lexical mappings rather than relying on cognate recognition.

**Productive Verbal Morphology.** The language employs a productive prefix system for verbs, particularly the "e-" prefix that indicates first-person subject agreement. For example, "emau" (I want) and "eti" (I go) demonstrate this morphological pattern. This agglutinative feature creates a larger effective vocabulary and requires the model to understand morphological composition rather than treating each word form as independent.

**Word Order Variations.** While both Indonesian and Papua Kokas generally follow Subject-Verb-Object (SVO) word order, Papua Kokas exhibits variations in constituent placement, particularly for adverbial phrases and question words.

The Transformer architecture, specifically the NLLB-200 model, accommodates these linguistic characteristics through several mechanisms. The subword tokenization using SentencePiece decomposes words into smaller units, allowing the model to recognize the "e-" verbal prefix as a recurring morphological pattern rather than treating each inflected form as a separate vocabulary item. This is evidenced by the high chrF++ score (79.45), which significantly exceeds the BLEU score (59.54), indicating strong character-level and morphological accuracy.

Multilingual transfer learning also plays a crucial role in the model's success. Although Papua Kokas is not among the 200+ languages in NLLB-200's pre-training, the model benefits from learned representations of other Austronesian languages that share similar grammatical structures. The Indonesian encoder provides robust representations for the source language, while the decoder adapts to Papua Kokas patterns through fine-tuning on the parallel corpus.

Furthermore, the self-attention mechanism enables the model to capture relationships between non-adjacent words, which is essential for correctly generating morphologically marked verbs that agree with their subjects regardless of intervening elements. Unlike RNN-based models that process sequences sequentially and may lose information over long distances, the Transformer's attention mechanism considers all positions simultaneously, providing a clear advantage for handling the complex morphological patterns of Papua Kokas.

### **Comparison with Previous Studies on Indonesian Regional Languages**

When compared to previous studies on Indonesian regional language translation, the results of this study demonstrate substantially improved performance. Earlier works focusing on Indonesian–Makassar translation using neural methods achieved BLEU scores in the range of 20-35 \[12\], while LSTM-based Indonesian–Madurese translation reported BLEU scores around 25-30 \[13\]. The NLLB-200 model's achievement of 59.54 BLEU in this study represents a significant advancement, attributable to the use of state-of-the-art multilingual Transformer architecture and effective transfer learning strategies.

Furthermore, pivot-based approaches for low-resource Indonesian language pairs have shown improvements but introduce additional complexity and potential error propagation \[15\]. The direct translation approach in this study demonstrates that single-stage Transformer fine-tuning can achieve competitive or superior results without requiring intermediate languages.

### **Limitations and Threats to Validity**

Despite the encouraging results, several limitations must be acknowledged. The dataset consists of 4,057 sentence pairs, primarily covering daily conversational expressions. As a result, the model's performance may degrade when translating more complex or domain-specific sentences. Stress testing revealed that the model exhibits repetition loops when processing complex compound sentences with long-range dependencies, indicating overfitting to the predominantly simple sentence structures in the training corpus.

The evaluation relied on automatic metrics (BLEU, chrF++, TER), which, while providing objective performance indicators, do not fully capture semantic adequacy, grammatical correctness, or cultural nuances. Human evaluation by native speakers remains essential for assessing translation naturalness and cultural appropriateness \[22\], \[23\], but was not conducted in this study due to resource constraints.

### **Implications for Language Revitalization**

Beyond technical performance, the findings of this study have broader implications for language revitalization efforts. The successful deployment of the translation model in a web-based application demonstrates how modern NMT technologies can be leveraged to support endangered languages in practical settings. The high chrF++ score (79.45) indicates that the model produces morphologically accurate output, which is particularly important for maintaining linguistic authenticity in revitalization efforts.

By demonstrating that Transformer-based NMT models significantly outperform traditional and RNN-based approaches in extremely low-resource contexts, this study provides empirical evidence supporting the use of multilingual pre-trained models for endangered language technology. The approach presented here can serve as a foundation for future initiatives aimed at digitizing and revitalizing other endangered regional languages in Indonesia and beyond.

## **Conclusions**

This study presented a comprehensive comparison of translation approaches for the endangered Papua Kokas language under low-resource conditions, evaluating word-based dictionary, LSTM sequence-to-sequence, and Transformer-based methods. By fine-tuning the multilingual NLLB-200 model on a manually collected parallel corpus of 4,057 sentence pairs, the proposed system achieved a BLEU score of 59.54, chrF++ of 79.45, and TER of 27.70, significantly outperforming both the LSTM baseline (BLEU 30.74) and word-based baseline (BLEU 19.23).

The experimental results provide clear empirical evidence that Transformer-based architectures with multilingual pre-training are substantially more effective than traditional and RNN-based approaches for low-resource translation tasks. The particularly high chrF++ score demonstrates the model's strength in capturing the morphological patterns unique to Papua Kokas, including verbal prefixes and distinct pronominal forms. These findings indicate that transfer learning from multilingual Transformer models plays a critical role in overcoming data scarcity for endangered language technology.

This study also contributes to the understanding of how Transformer architectures accommodate the specific linguistic characteristics of under-documented languages. The subword tokenization mechanism effectively handles productive morphology, while self-attention captures the grammatical patterns necessary for accurate translation. These insights can inform future NMT development for other endangered languages with similar morphological complexity.

Beyond quantitative performance, the deployment of the trained model in a web-based application highlights the practical feasibility of applying NMT technologies to real-world language revitalization. Such tools can facilitate access to information, promote digital usage of local languages, and encourage intergenerational language transmission.

Despite these contributions, this study is subject to several limitations, including the conversational domain focus of the dataset and the reliance on automatic evaluation metrics. Future research should focus on expanding the parallel corpus to cover more domains, incorporating human evaluation by native speakers, and addressing the repetition issues observed in complex sentences. Extending this comparative approach to other endangered regional languages may further strengthen the role of Neural Machine Translation in supporting linguistic diversity and cultural sustainability.

### **Additional Information**

**Author Contributions:**

* \[First Author\]: Conceptualization, Methodology, Formal Analysis, Writing – Original Draft, Writing – Review & Editing.  
* \[Second Author\]: Software, Model Implementation, Experimentation, Validation, Visualization.  
* \[Third Author\]: Data Collection, Data Curation, Linguistic Resource Preparation.

**Funding:** This research was self-funded by the authors. The article publication fee was supported by the Ministry of Higher Education, Science, and Technology of the Republic of Indonesia, Directorate General of Research and Development, through the 2025 Reputable Journal Publication Assistance Program.

**Conflicts of Interest:** The authors declare no conflict of interest.

**Data Availability:** The dataset used in this study consists of parallel Indonesian–Papua Kokas sentences collected through interviews with native speakers. Due to ethical considerations and the protection of indigenous language resources, the data are not publicly available. Access to the data may be considered upon reasonable request to the corresponding author.

**Informed Consent:** Informed consent was obtained from all participants involved in the data collection process. The purpose of the study and the use of the collected linguistic data were clearly explained to the participants prior to data collection.

**Institutional Review Board Statement:** This study did not require formal ethical approval, as it involved linguistic data collection through voluntary participation without recording personal or sensitive information.

**Animal Subjects:** There were no animal subjects.

**ORCID:**

* First Author: [https://orcid.org/0000-0003-1643-4252](https://orcid.org/0000-0003-1643-4252)  
* Second Author: [https://orcid.org/0000-0002-1848-167X](https://orcid.org/0000-0002-1848-167X)  
* Third Author: \-

### **References**

1. A. F. Aji et al., “One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia,” in *Proceedings of the Annual Meeting of the Association for Computational Linguistics*, 2022, pp. 7226–7249. DOI: 10.18653/v1/2022.acl-long.500.  
2. B. Huszka, A. Stark, and I. Aini, “Linguistic Sustainability: Challenges and Strategies of Preserving Minority and Indigenous Languages – The Case of Indonesia,” *Int. J. Arts Soc. Sci.*, vol. 7, no. 6, pp. 147–160, 2024\.  
3. S. B. Dahal and M. Aoun, “Exploring the Role of Machine Translation in Improving Health Information Access for Linguistically Diverse Populations,” *Adv. Intell. Inf. Syst.*, vol. 8, no. 2, pp. 1–13, 2022\.  
4. N. Katiyar, S. Jain, A. Gupta, M. Tiwari, R. Mishra, and S. Chaurasia, “Breaking Language Barriers: Advancements in Machine Translation for Enhanced Cross-Lingual Information Retrieval,” *J. Electr. Syst.*, pp. 2860–2875, 2024\.  
5. E. Steigerwald, V. Ramírez-castañeda, D. Y. C. Brandt, and A. Báldi, “Overcoming Language Barriers in Academia : Machine Translation Tools and a Vision for a Multilingual Future,” vol. 72, no. 10, 2022\. DOI: 10.1093/biosci/biac062.  
6. W. Zhang, “Applications of Deep Learning in Natural Language Processing: A Case Study on Machine Translation,” *J. Comput. Signal, Syst. Res.*, vol. 2, no. 1, pp. 1–11, 2025\. DOI: 10.71222/acs2j404.  
7. N. Shahin and L. Ismail, “From Rule ‑ based Models to Deep Learning Transformers Architectures for Natural Language Processing and Sign Language Translation systems: survey, taxonomy and performance evaluation,” *Deaf or Hard of Hearing*, vol. 57, no. 10\. Springer Netherlands, 2024\. DOI: 10.1007/s10462-024-10895-z.  
8. A. Magueresse, V. Carles, and E. Heetderks, “Low-resource Languages: A Review of Past Work and Future Challenges,” *arXiv Prepr. arXiv2006.07264*, 2020\. DOI: 10.48550/arXiv.2006.07264.  
9. R. K. Dwivedi, P. Nand, and O. Pal, “Hybrid NMT model and comparison with existing machine translation approaches,” *Multidiscip. Sci. J.*, vol. 7, no. 4, 2025\. DOI: 10.31893/multiscience.2025146.  
10. J. V. C. I. R, C. Su, H. Huang, S. Shi, P. Jian, and X. Shi, “Neural machine translation with Gumbel Tree-LSTM based encoder,” *J. Vis. Commun. Image Represent.*, vol. 71, p. 102811, 2020\. DOI: 10.1016/j.jvcir.2020.102811  
11. A. Rahali and M. A. Akhloufi, “End-to-End Transformer-Based Models in Textual-Based NLP,” *AI*, vol. 4, no. 1, pp. 54–110, 2023\. DOI: 10.3390/ai4010004.  
12. D. I. N. Afra et al., “Neural Machine Translation for Low-Resource Languages: Experiments on Makassar-Indonesian,” in *International Conference on Computer, Control, Informatics and its Applications (IC3INA)*, 2024, pp. 66–71. DOI: 10.1109/IC3INA64086.2024.10732202.  
13. D. A. Sulistyo, A. P. Wibawa, D. D. Prasetya, and F. A. Ahda, “LSTM-Based Machine Translation for Madurese-Indonesian,” *J. Appl. Data Sci.*, vol. 4, no. 3, pp. 190–199, 2023\. DOI: 10.47738/jads.v4i3.113.  
14. M. Rehan, M. S. I. Malik, and M. M. Jamjoom, “Fine-Tuning Transformer Models Using Transfer Learning for Multilingual Threatening Text Identification,” *IEEE Access*, vol. 11, no. August, pp. 106503–106515, 2023\. DOI: 10.1109/ACCESS.2023.3320062.  
15. D. A. Sulistyo, A. P. Wibawa, D. D. Prasetya, and F. A. Ahda, “An Enhanced Pivot-Based Neural Machine Translation for Low-Resource Languages,” *Int. J. Adv. Intell. Informatics*, vol. 11, no. 2, pp. 258–274, 2025\. DOI: 10.26555/ijain.v11i2.2115.  
16. C. Han and X. Lu, “Beyond BLEU : Repurposing Neural-Based Metrics to Assess Interlingual Interpreting in Tertiary-Level Language Learning Settings,” *Res. Methods Appl. Linguist.*, vol. 4, no. 1, p. 100184, 2025\. DOI: 10.1016/j.rmal.2025.100184.  
17. G. Datta, N. Joshi, and K. Gupta, “Human Versus Automatic Evaluation of NMT for Low-Resource Indian Language,” in *Proceedings of International Conference on Recent Innovations in Computing*, 2025, pp. 715–725. DOI: 10.1007/978-981-99-0601-7\_55.  
18. X. Wu and R. Deng, “Research on the Application of Cross-Language Transfer Learning Model in English Translation for Low-Resource Scenarios,” *IEEE Access*, vol. 13, no. September, pp. 201960–201976, 2025\. DOI: 10.1109/ACCESS.2025.3628643.  
19. P. K. Myakala and P. Naayini, “Bridging the Gap: Leveraging Transfer Learning for Low-Resource NLP Tasks,” *Int. J. Comput. Tech.*, vol. 10, no. 5, 2023\.  
20. E. Agyei, X. Zhang, A. B. Quaye, V. A. Odeh, and J. R. Arhin, “Dynamic Aggregation and Augmentation for Low-Resource Machine Translation Using Federated Fine-Tuning of Pretrained Transformer Models,” *Appl. Sci.*, vol. 15, pp. 1–26, 2025\. DOI: 10.3390/app15084494.  
21. T. Adimulam, S. Chinta, and S. K. Pattanayak, “Transfer Learning in Natural Language Processing: Overcoming Low-Resource Challenges,” *Int. J. Enhanc. Res. Sci. Technol. Eng.*, vol. 11, no. 2, pp. 65–79, 2022\. DOI: 10.0/ste/22.02.09.  
22. M. Vulchanova, V. Vulchanov, A. Sorace, and C. Suarez-gomez, “Editorial: The Notion of the Native Speaker Put to the Test: Recent Research Advances,” *Front. Psychol.*, vol. 13, pp. 1–6, 2022\. DOI: 10.3389/fpsyg.2022.875740.  
23. G. Bella, P. Helm, G. Koch, and F. Giunchiglia, "Tackling Language Modelling Bias in Support of Linguistic Diversity," in *FAccT '24: The 2024 ACM Conference on Fairness, Accountability, and Transparency*, ACM, 2024\. DOI: 10.1145/3630106.3658925
24. NLLB Team et al., "No Language Left Behind: Scaling Human-Centered Machine Translation," *arXiv preprint arXiv:2207.04672*, 2022\. DOI: 10.48550/arXiv.2207.04672.
25. M. Popović, "chrF: character n-gram F-score for automatic MT evaluation," in *Proceedings of the Tenth Workshop on Statistical Machine Translation*, 2015, pp. 392–395. DOI: 10.18653/v1/W15-3049.
26. M. Snover, B. Dorr, R. Schwartz, L. Micciulla, and J. Makhoul, "A Study of Translation Edit Rate with Targeted Human Annotation," in *Proceedings of the 7th Conference of the Association for Machine Translation in the Americas*, 2006, pp. 223–231.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAaCAYAAABsONZfAAAAyklEQVR4XmNgGDpAUVHRTl5efhYWXKqgoMABwuh6wEBOTi4MhIEKb8jKyiqDMLoaDECWJqDiViheA+SyQDFuAHIzUPFWKC5Cl8cKyNIkLS0tA/ILCAP9ZYMujxUAFboANdwFYZAB6PJYAVmaQP6A+Qk9IoERrw/CQHFzmBg4aEHBLA8NciT1IMAIFMuCYkWwiJSUlAgIAwWuACPTD4SRdQDFrYB4KggzwOKNZE0gBUDOdij+C8TroRiUUE9D8T+gXyJAGNmwUTAMAQAR50PkM11ECgAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAABJUlEQVR4Xu2SOy8GURCGV5AQCQlik72ds5dGo9noKCSiU2mI2qWgFolOo5fwC3SU29MoNFqln+J5184XxNfYSniTJ3vOzLwze/ZsEPzrN6mu63GRJMks25Gv+aHK89xlWXYhnHON937bcsRqeBBxHM999LXqZSaxj2mxo4Fdy9HogP2NCL47ThiGU0xfEhQ9Q054TLC+VQOh2jRNN3yn/mbJClQsUxRF84LYE8daEawnyF8yJBQDM8kTQ3uK1oTMNon9GTyy3BGUjZp5XZC8J3HI86WjfRPR5Y8GE00/NvNXTfIhlkVVVdNlWS5QdCf85zs/1tm570RYcJPCV6EfBm259/tuiqKYMTONTqndY8iqaIPqQvBaYLiCc12fMONQ9TL/Qb0BtPlhFkATA3gAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAABC0lEQVR4XmNgGBlAXl5eEoh7oXgWFJeCsIKCAgcQRyCJg3ANCIuLi3Ojm8UAEgRhoIK1QI2npKSkREAYJAcUUwTiPSAMlLM3NjZmBWF0M1AAUKEHUMMnILYEYSUlJX45ObnpioqK8iCMrh4noJpBIO8ADbgKxLOhuBqINdHVEQWArmoAav4NxY7o8sQCRqBXyoAG/ANhUIyhKyAWUGwQIwgDNQYADQgC4uUgDDR0h4yMDCe6YpwAqjkIaFABA8RAD+QYRFePFQBtdQEqLgJhWEKDJUh5SAxOYYC6GFUnGqDIIGj+OQ3F/4F4PQirqKjwAaVZ5CHpB4S/AfEvIF4GwsBEqY5u1igYBZQCAILYVFVTyy51AAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAYCAYAAABjswTDAAABtElEQVR4Xu2VsS8EQRjF92IVQkhwlt29nd29ayg0G9GQIBIi0aCQXKVBo74/QKNVcI3mJCpHKC5aWg2l0p/ivbuZZE3WcVGck3nJLzfzzffNvJ2bnbUsIyMjo95UkiT9xPf9UXRz+vifURRFIgiCEyKEaIRhuKvGEEvAk+d5YyRd1xXBzD5MTksaoKzGYPwA/Surtdvd3/GeMus4ziCOwiyBsRcQIWwTtOs0zLNM0N5D7BZMEX0uCnkDhA/NufXxNrIx/xrqLiUbekJTNCR3sY6u7bruOEHsGTu/oPLy+fwQYrV2ZoX8l1BXtVoP3ZFQV5Fs6mNNpRIq7GOxZUKzNK3ysswWCoVFtC8kK+BBcs2dUrU/1b8zu0qwwCMWOMTvm6R5LFRellnezzyb8nzmMH5KMF/CcbQnCfK3ENvR4cMSpPZJL1+b5cuA5DlSKpWGi8XiBCa+IWHqzqWyzKYlz3mN4IV1snK+U1uzDGLSd8IPBLQtWldYI47jEeao2wCxMnhFzRFBzIOxdbTvJDOgShjv0CxvgyXU3hPUnqE//ymjp8ziM+qrBZBwDo5TZ9DIyOgX+gBXwaCD3MdHxgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,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>