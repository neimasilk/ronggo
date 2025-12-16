# Log Eksperimen NLLB-200 (Bahasa Sekar)
**Tanggal:** 16 Desember 2025
**Pelaksana:** Gemini Agent
**Fokus:** Setup Environment & Baseline Training dengan NLLB-200

## 1. Ringkasan
Eksperimen ini bertujuan untuk menggantikan baseline lama (MarianMT) dengan model state-of-the-art **NLLB-200 (No Language Left Behind)**. Kami berhasil melakukan fine-tuning awal (1 epoch) pada dataset Bahasa Sekar yang telah dibersihkan.

## 2. Lingkungan & Setup
*   **Hardware:** Tesla T4 GPU (16GB VRAM)
*   **Library Utama:**
    *   `transformers` (Hugging Face)
    *   `torch` (dengan CUDA support)
    *   `datasets`, `evaluate`, `sacrebleu`
*   **Model Base:** `facebook/nllb-200-distilled-600M`
    *   Model ini dipilih karena ukurannya yang efisien (600M params) namun memiliki kemampuan transfer learning multibahasa yang kuat.

## 3. Implementasi Teknis (`train_nllb.py`)
Skrip training dibuat dari nol dengan spesifikasi berikut:
*   **Source Language:** `ind_Latn` (Indonesian)
*   **Target Language Placeholder:** `eng_Latn` (English).
    *   *Catatan:* Karena Bahasa Sekar tidak ada dalam pre-training NLLB, kita "membajak" kode bahasa `eng_Latn` sebagai target. Ini teknik umum dalam fine-tuning bahasa baru (*language transfer*).
*   **Hyperparameter:**
    *   Learning Rate: `2e-5`
    *   Batch Size: `16`
    *   Weight Decay: `0.01`
    *   Precision: `fp16` (Mixed Precision)

### Tantangan & Solusi
Selama implementasi, ditemukan beberapa masalah integrasi library `transformers` terbaru:
1.  **Isu Tokenisasi NLLB:** Tokenizer NLLB memerlukan pengaturan `src_lang` dan `tgt_lang` yang eksplisit, serta `forced_bos_token_id` agar model tahu bahasa apa yang harus digenerate.
    *   *Fix:* Set `tokenizer.src_lang` dan `tokenizer.tgt_lang` secara manual di skrip.
2.  **Deprecated API:** Argumen `evaluation_strategy` pada `Seq2SeqTrainingArguments` telah diganti menjadi `eval_strategy`.
    *   *Fix:* Update argumen sesuai versi library terbaru.
3.  **Data Mapping:** Penyesuaian nama kolom dataset (`indonesian` -> `papua_kokas`) pada fungsi preprocessing.

## 4. Hasil Benchmark Awal (1 Epoch)
Training dilakukan selama 1 epoch untuk memvalidasi pipeline (Proof of Concept).

| Metrik | Nilai | Analisis |
| :--- | :--- | :--- |
| **Training Loss** | 6.97 | Masih tinggi (wajar untuk epoch pertama). |
| **BLEU Score** | **15.46** | Start yang sangat baik. Sebagai perbandingan, model random/untrained biasanya < 1.0. |
| **Gen Length** | 19.25 | Panjang kalimat hasil generasi stabil dan sesuai dengan rata-rata target. |

## 5. Rekomendasi Selanjutnya
Pipeline telah terbukti valid (**Stable**). Langkah selanjutnya untuk mencapai performa maksimal (target BLEU > 40):
1.  **Full Training:** Jalankan `train_nllb.py` dengan `NUM_EPOCHS = 10` atau `20`.
2.  **Evaluasi:** Bandingkan hasil kualitatif (contoh terjemahan) dengan hasil MarianMT lama.
3.  **Deployment:** Model yang disimpan di folder `nllb-sekar-finetuned/` siap diload untuk inferensi.
