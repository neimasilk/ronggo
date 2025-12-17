# Ide Eksperimen Lanjutan: Peningkatan Model MT Bahasa Sekar

Meskipun model NLLB-200 mencapai BLEU score **60.05**, masih ada ruang untuk perbaikan, terutama dalam hal ketahanan (*robustness*) terhadap kalimat yang tidak biasa dan validasi metrik yang mungkin terlalu optimis karena dataset yang kecil.

## 1. Validasi Metrik (Priority: High)
Skor BLEU > 60 pada *low-resource language* seringkali mengindikasikan *data leakage* atau overlap yang tinggi antara data train dan test.
*   **Analisis N-Gram Overlap:** Cek seberapa banyak frasa di `test.csv` yang persis sama dengan di `train.csv`.
*   **K-Fold Cross Validation:** Lakukan 5-fold CV untuk memastikan skor BLEU konsisten di seluruh bagian data, bukan kebetulan pada split tertentu.

## 2. Data Augmentation
Untuk mengatasi kelangkaan data (~3000 kalimat):
*   **Back-Translation:**
    1.  Latih model Sekar -> Indonesia (Reverse Model).
    2.  Gunakan model tersebut untuk menerjemahkan kalimat monolingual Indonesia (dari korpus berita/umum) ke Bahasa Sekar (sintetis).
    3.  Latih ulang model Indonesia -> Sekar dengan data campuran (Asli + Sintetis).
*   **Synonym Replacement:** Ganti kata-kata tertentu dalam kalimat sumber (Indonesia) dengan sinonimnya untuk memperkaya variasi input.

## 3. Eksplorasi Arsitektur Model
*   **NLLB-1.3B:** Jika sumber daya komputasi memungkinkan (GPU dengan VRAM > 24GB), coba gunakan model NLLB varian 1.3 Miliar parameter.
*   **Multilingual Training:** Jika ada bahasa daerah Papua lain yang serumpun dan memiliki data, coba latih model secara bersamaan (*multi-task learning*) agar model mempelajari fitur linguistik regional.

## 4. Human-in-the-Loop Evaluation
BLEU score tidak selalu mencerminkan kualitas terjemahan yang luwes.
*   Buat antarmuka sederhana (Streamlit/Gradio).
*   Minta penutur asli untuk memberi rating (1-5) pada hasil terjemahan model.
*   Gunakan feedback ini untuk *Reinforcement Learning* (RLHF) di masa depan.
