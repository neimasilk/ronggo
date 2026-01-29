# Detail Eksperimen Lanjutan

Dokumen ini berisi detail teknis untuk fase pengembangan berikutnya.

## EXP-003: LLM-Based Data Augmentation (In Progress)
Mengatasi masalah *data scarcity* dan *overfitting* dengan memperkaya data training secara sintetis.

### Metodologi
1.  **Source:** `dataset/train.csv` (Bahasa Indonesia).
2.  **Tools:** DeepSeek V3 API (via OpenAI SDK).
3.  **Prompt Strategy:**
    *   Input: Kalimat Indonesia asli (misal: "Saya makan nasi").
    *   Task: "Parafrase kalimat ini agar strukturnya berbeda tapi maknanya sama."
    *   Output: Kalimat variasi (misal: "Aku sedang menyantap hidangan nasi").
    *   **Invariance Assumption:** Terjemahan Bahasa Sekar diasumsikan tetap sama untuk kedua variasi tersebut.
4.  **Target Dataset:**
    *   Ukuran: ~6.500 pasang kalimat (2x lipat dari original).
    *   Tujuan: Memaksa model NLLB belajar memetakan *banyak* variasi input Indonesia ke *satu* output Sekar yang benar (*Many-to-One*).

## EXP-004: Retraining NLLB with Augmented Data
Setelah dataset augmented siap:
1.  Latih ulang NLLB-200 dari checkpoint awal.
2.  Bandingkan performa pada **Test Set Lama** vs **Hard Test Set**.
3.  Hipotesis: Skor BLEU mungkin sedikit turun di Test Set Lama (karena model kurang "hafal"), tapi kualitas terjemahan pada kalimat baru (unseen) akan meningkat drastis.

## EXP-005: Hard Test Set Creation
Membuat benchmark evaluasi yang jujur.
*   **Metode:** Ambil daftar kata dasar Bahasa Sekar, lalu susun kalimat Indonesia baru yang menggunakan kata-kata tersebut dalam kombinasi yang *belum pernah ada* di training data.
*   **Tujuan:** Mengukur kemampuan generalisasi tata bahasa yang sebenarnya.
