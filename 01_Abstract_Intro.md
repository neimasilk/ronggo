# Abstract

The preservation of indigenous languages is a critical challenge in the digital age, particularly for under-resourced languages like Papua Kokas, a language spoken in the Fakfak regency of West Papua, Indonesia. This paper presents a Neural Machine Translation (NMT) system designed to facilitate the revitalization of the Papua Kokas language by enabling automatic translation from Indonesian. Utilizing a low-resource NMT approach, we employ Transfer Learning with a Transformer-based architecture. Specifically, we fine-tune the MarianMT model, originally pre-trained on a larger Indonesian-English corpus, using a manually curated dataset of 2,909 Indonesian-Kokas sentence pairs. Our experiments demonstrate the feasibility of this approach, achieving a BLEU score of 46.73, which indicates a high degree of translation quality despite the limited data availability. This work contributes to the digital documentation of the Papua Kokas language and provides a framework for developing translation tools for other endangered languages in the region.

**Keywords**: Neural Machine Translation, Low-Resource Languages, Transformers, Transfer Learning, Papua Kokas, Language Preservation.

# 1. Introduction

Indonesia is a linguistically diverse nation with over 700 distinct languages. However, a significant number of these languages are currently endangered due to the declining number of native speakers and the dominance of the national language, Indonesian (Bahasa Indonesia). The Papua Kokas language (also known as Sekar), spoken in the Kokas District of Fakfak Regency, West Papua, faces similar threats of attrition. Revitalizing such languages requires not only documentation but also the development of digital tools that can bridge the gap between the younger generation and their ancestral tongue.

Machine Translation (MT) offers a powerful solution for language revitalization, enabling real-time communication and learning. However, modern Neural Machine Translation (NMT) models, such as the Transformer architecture proposed by Vaswani et al. (2017), typically require massive parallel corpora (millions of sentence pairs) to achieve fluency and accuracy. For a low-resource language like Papua Kokas, where available digitized text is scarce, training an NMT model from scratch is often infeasible.

To address this challenge, this study adopts a Transfer Learning approach. We leverage a pre-trained Transformer model (MarianMT) that has already learned the linguistic features of Indonesian. By fine-tuning this model on a small, high-quality corpus of Indonesian-Kokas pairs, we aim to transfer the encoder's understanding of Indonesian to generate Kokas translations effectively.

The primary contributions of this paper are:
1.  **Dataset Construction**: The curation and preprocessing of a parallel corpus containing 2,909 sentences mapping Indonesian to Papua Kokas.
2.  **Model Implementation**: The adaptation of a Transformer-based NMT model for the specific low-resource context of the Kokas language.
3.  **Evaluation**: A comprehensive evaluation of the model's performance using the BLEU metric, demonstrating the potential of transfer learning for extremely low-resource settings.

The remainder of this paper is organized as follows: Section 2 reviews related work in low-resource NMT. Section 3 details the methodology, including dataset preparation and model architecture. Section 4 presents the experimental setup and results. Finally, Section 5 concludes the study and outlines future directions.
