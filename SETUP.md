# Panduan Setup Proyek (Environment Guide)

Proyek ini mendukung dua lingkungan kerja utama: **Google Colab** dan **Komputer Pribadi (Local Linux)**.

## Opsi A: Google Colab (Cloud)
Lingkungan ini bersifat sementara (ephemeral). Gunakan script ini setiap kali memulai sesi baru.

1.  Mount Google Drive.
2.  Buka terminal (atau cell notebook) dan masuk ke direktori proyek.
3.  Jalankan setup otomatis:
    ```bash
    !bash setup_colab.sh
    ```
4.  **API Keys:** Masukkan key secara manual saat menjalankan script, atau gunakan Google Colab Secrets.

## Opsi B: Komputer Pribadi (Local Linux)
Lingkungan ini persisten. Kita menggunakan Virtual Environment (`.venv`) agar sistem Python utama Anda tetap bersih.

1.  **Pertama Kali Setup:**
    ```bash
    bash setup_local.sh
    ```
    *Script ini akan membuat folder `.venv`, menginstall library, dan membuat file template `.env`.*

2.  **Aktifkan Environment:**
    Setiap kali Anda membuka terminal baru, jalankan:
    ```bash
    source .venv/bin/activate
    ```

3.  **Konfigurasi API Key:**
    Edit file `.env` yang baru dibuat, masukkan API Key Anda:
    ```ini
    GEMINI_API_KEY=AIzaSy...
    DEEPSEEK_API_KEY=sk-...
    ```
    *File `.env` otomatis diabaikan oleh git (aman).*

4.  **Menjalankan Generator:**
    Karena sudah ada `.env`, Anda tidak perlu mengetik key lagi:
    ```bash
    python dataset/scripts/generate_synthetic_llm.py --provider gemini --count 50
    ```
