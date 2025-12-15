# 5. Conclusion and Future Work

## 5.1 Conclusion
This research presented a successful implementation of a Neural Machine Translation system for the endangered Papua Kokas language. By employing a Transfer Learning approach with the MarianMT Transformer model, we overcame the significant hurdle of data scarcity. With a curated dataset of only 2,909 sentence pairs, the model achieved a remarkable BLEU score of **46.73**. This result confirms that pre-trained models, even when trained on related but distinct languages (like Indonesian-English), can be effectively repurposed for local language revitalization tasks. This project serves as a proof-of-concept for digital preservation efforts for other regional languages in Indonesia.

## 5.2 Future Work
While the current results are promising, several avenues for improvement exist:
1.  **Dataset Expansion**: Continuous collection of more diverse parallel texts will improve the model's vocabulary and robustness.
2.  **Application Deployment**: Integrating the model into a user-friendly mobile application or a public web interface (as demonstrated in our preliminary web app) to make the tool accessible to the Kokas community.
3.  **Speech Translation**: Given that many indigenous languages are primarily oral, extending the system to include Speech-to-Text (ASR) and Text-to-Speech (TTS) capabilities would significantly enhance its utility for language learning and documentation.

# References
[1] Vaswani, A., et al. (2017). "Attention Is All You Need". Advances in Neural Information Processing Systems.
[2] Junczys-Dowmunt, M., et al. (2018). "Marian: Fast Neural Machine Translation in C++". Proceedings of ACL 2018.
[3] Zoph, B., et al. (2016). "Transfer Learning for Low-Resource Neural Machine Translation". EMNLP.
