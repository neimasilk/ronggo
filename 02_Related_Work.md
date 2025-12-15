# 2. Related Work

## 2.1 Neural Machine Translation and Transformers
Neural Machine Translation (NMT) has revolutionized the field of automated translation, surpassing statistical methods in fluency and context handling. The introduction of the Transformer architecture [Citation: Vaswani et al., 2017] marked a significant milestone. Relying entirely on self-attention mechanisms rather than recurrent or convolutional layers, Transformers allow for parallelization during training and better handling of long-range dependencies in sentences. This architecture has become the de facto standard for NMT tasks.

## 2.2 Low-Resource NMT
The primary bottleneck for NMT is the requirement for large-scale parallel corpora. "Low-resource" languages are those lacking such massive datasets. Research in this area focuses on techniques to maximize performance with limited data. Zoph et al. [Citation] demonstrated the effectiveness of Transfer Learning, where a parent model trained on a high-resource language pair is fine-tuned on the low-resource pair. This approach allows the model to leverage general linguistic properties (syntax, semantics) learned from the parent task.

## 2.3 MarianMT Framework
MarianMT [Citation: Junczys-Dowmunt et al., 2018] is an efficient NMT framework written in C++ that has been widely adopted by the research community, particularly through the Helsinki-NLP project. It provides a vast repository of pre-trained models for thousands of language pairs. Its compatibility with the Hugging Face Transformers library makes it an ideal candidate for fine-tuning tasks. In this study, we utilize the `opus-mt-id-en` model as our starting point, leveraging its pre-existing knowledge of the Indonesian language to facilitate the translation into Papua Kokas.
