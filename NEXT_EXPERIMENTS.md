# Ide Eksperimen Lanjutan: Peningkatan Model MT Bahasa Sekar

Meskipun model NLLB-200 mencapai BLEU score **60.05**, masih ada ruang untuk perbaikan, terutama dalam hal ketahanan (*robustness*) terhadap kalimat yang tidak biasa dan validasi metrik yang mungkin terlalu optimis karena dataset yang kecil.

## 1. Validasi Metrik (Priority: High)
Skor BLEU > 60 pada *low-resource language* seringkali mengindikasikan *data leakage* atau overlap yang tinggi antara data train dan test.
*   **Analisis N-Gram Overlap:** Cek seberapa banyak frasa di `test.csv` yang persis sama dengan di `train.csv`.
*   **K-Fold Cross Validation:** Lakukan 5-fold CV untuk memastikan skor BLEU konsisten di seluruh bagian data, bukan kebetulan pada split tertentu.

## 2. Data Augmentation (Active Phase)
Untuk mengatasi kelangkaan data (~3000 kalimat) dan masalah *repetition loop* pada kalimat kompleks:

*   **Strategi Utama: LLM-Based Generation (Closed Vocabulary)**
    *   Menggunakan Gemini/DeepSeek untuk generate kalimat majemuk.
    *   **Strict Constraint:** Menggunakan "Kamus Putih" (White-list) dari data latih. Jika kata tidak ada di kamus, wajib *fallback* ke Bahasa Indonesia (Code Mixing) untuk mencegah halusinasi.
    *   **NER Preservation:** Nama orang/kota tidak boleh diterjemahkan.

*   **Strategi Cadangan: Back-Translation**
    *   (Deprioritized) Hanya dilakukan jika metode LLM gagal menghasilkan variasi struktur yang cukup.

*   **Synonym Replacement:** 
    *   Ganti kata-kata tertentu dalam kalimat sumber (Indonesia) dengan sinonimnya untuk memperkaya variasi input.

## 3. Eksplorasi Arsitektur Model
*   **NLLB-1.3B:** Jika sumber daya komputasi memungkinkan (GPU dengan VRAM > 24GB), coba gunakan model NLLB varian 1.3 Miliar parameter.
*   **Multilingual Training:** Jika ada bahasa daerah Papua lain yang serumpun dan memiliki data, coba latih model secara bersamaan (*multi-task learning*) agar model mempelajari fitur linguistik regional.

## 4. Human-in-the-Loop Evaluation
BLEU score tidak selalu mencerminkan kualitas terjemahan yang luwes.
*   Buat antarmuka sederhana (Streamlit/Gradio).
*   Minta penutur asli untuk memberi rating (1-5) pada hasil terjemahan model.
*   Gunakan feedback ini untuk *Reinforcement Learning* (RLHF) di masa depan.
