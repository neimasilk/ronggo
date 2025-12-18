# Eksperimen 02: Synthetic Data Augmentation (LLM & Hybrid)

**Status:** Active
**Branch:** `exp/synthetic-data`

## Tujuan
Meningkatkan performa model NLLB-200, secara spesifik mengatasi masalah **Repetition Loop pada kalimat kompleks**, dengan memperbesar dataset menggunakan bantuan Large Language Models (LLM).

## Strategi Utama: "Closed Vocabulary & Code Mixing"
Kita menggunakan pendekatan yang sangat ketat untuk mencegah halusinasi model (mengingat data Bahasa Sekar sangat terbatas).

### 3 Aturan Emas (The 3 Golden Rules)
Script generator (`generate_synthetic_llm.py`) dirancang untuk mematuhi aturan ini:

1.  **Complexity First:** Target kalimat adalah majemuk/kompleks (menggunakan kata sambung "dan", "tetapi", "karena", "walaupun") untuk melatih model menangani struktur sintaksis yang rumit.
2.  **NER Preservation:** Entitas Nama (Orang, Kota, Negara) **DILARANG** diterjemahkan. Harus persis sama dengan Bahasa Indonesia.
3.  **Dictionary Check (Closed Vocab):**
    *   Sistem memuat daftar kata valid dari `train.csv` (`known_vocab.json`).
    *   Jika LLM ingin menerjemahkan kata tapi tidak ada di daftar valid -> **WAJIB Fallback ke Bahasa Indonesia**.
    *   Ini disebut *Code Mixing*, strategi yang valid untuk bahasa daerah modern dan mencegah terciptanya kata-kata palsu.

## Rencana Kerja
1.  **Dictionary Build:** Ekstrak semua kata unik dari `train.csv` ke `known_vocab.json`. (Selesai)
2.  **Generation:** Gunakan LLM (Gemini/DeepSeek) dengan Prompt yang menyuntikkan (inject) daftar kosa kata tersebut.
3.  **Training:** Fine-tune NLLB dengan dataset campuran.

## File Struktur
*   `dataset/scripts/build_dictionary.py`: Ekstraktor kosa kata valid.
*   `dataset/scripts/generate_synthetic_llm.py`: Generator data dengan logika "Dry Run" dan integrasi API.
*   `dataset/known_vocab.json`: (Generated) Daftar kata putih (whitelist).
