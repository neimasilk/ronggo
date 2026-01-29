import pandas as pd

def main():
    print("--- Audit Konsistensi Dataset ---")
    
    try:
        df = pd.read_csv("dataset/master.csv")
    except:
        return

    # Cari source yang sama tapi target beda
    duplicates = df[df.duplicated(subset=['indonesian'], keep=False)]
    
    inconsistent = []
    grouped = duplicates.groupby('indonesian')
    
    for name, group in grouped:
        unique_targets = group['papua_kokas'].unique()
        if len(unique_targets) > 1:
            inconsistent.append({
                'indonesian': name,
                'targets': list(unique_targets)
            })

    print(f"Ditemukan {len(inconsistent)} kalimat Indonesia dengan terjemahan Sekar yang berbeda-beda.")
    
    if inconsistent:
        print("\nContoh Ketidakkonsistenan:")
        for item in inconsistent[:5]:
            print(f"\nSource: {item['indonesian']}")
            for i, tgt in enumerate(item['targets']):
                print(f"  Target {i+1}: {tgt}")

    # Simpan laporan
    with open("dataset/consistency_report.txt", "w", encoding="utf-8") as f:
        f.write("# Laporan Ketidakkonsistenan Dataset\n\n")
        for item in inconsistent:
            f.write(f"Source: {item['indonesian']}\n")
            for tgt in item['targets']:
                f.write(f"  - {tgt}\n")
            f.write("-" * 20 + "\n")

if __name__ == "__main__":
    main()
