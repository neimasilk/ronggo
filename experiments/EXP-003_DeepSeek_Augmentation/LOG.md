# LOG Eksperimen EXP-003: Data Augmentation with DeepSeek LLM

**Tanggal:** 29 Januari 2026
**Status:** Completed
**Peneliti:** Gemini Agent

## 1. Tujuan
Meningkatkan variasi dataset training tanpa menambah data manual. Tujuannya adalah memecah pola hafalan model dengan memberikan berbagai variasi kalimat Bahasa Indonesia untuk satu target Bahasa Sekar yang sama (Many-to-One mapping).

## 2. Metodologi
*   **Model:** DeepSeek-V3 (via OpenAI SDK).
*   **Teknik:** Paraphrasing pada 3.239 kalimat Bahasa Indonesia di `train.csv`.
*   **Input:** Kalimat asli Indonesia.
*   **Output:** Kalimat variasi Indonesia dengan makna yang sama.

## 3. Hasil
*   **Total Data Terproses:** 3.239 baris.
*   **Total Output:** 6.478 baris (Original + Augmented).
*   **Kualitas:** Sampling menunjukkan parafrase yang sangat berkualitas (penggunaan sinonim seperti "gemar", "wahana awal", "berkeinginan").

## 4. Dampak
Dataset training kini memiliki diversitas linguistik yang lebih luas. Hal ini diharapkan akan meningkatkan *robustness* model NLLB pada fase training selanjutnya (EXP-004).
