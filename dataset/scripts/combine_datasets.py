import pandas as pd
import glob
import os

# CONFIGURATION
PRIMARY_DATA = "../train.csv"
SYNTHETIC_DIR = "../synthetic/"
OUTPUT_FILE = "../train_augmented.csv"

def combine_data():
    print("=== DATASET COMBINATION UTILITY ===")
    
    # 1. Load Primary Data
    if not os.path.exists(PRIMARY_DATA):
        print(f"Error: Primary data not found at {PRIMARY_DATA}")
        return

    print(f"Loading Primary Data: {PRIMARY_DATA}")
    df_primary = pd.read_csv(PRIMARY_DATA)
    df_primary['source'] = 'original' # Tagging source
    print(f"  -> Loaded {len(df_primary)} rows.")

    # 2. Load Synthetic Data
    synthetic_files = glob.glob(os.path.join(SYNTHETIC_DIR, "*.csv"))
    df_synthetic_list = []
    
    print(f"Loading Synthetic Data from: {SYNTHETIC_DIR}")
    if not synthetic_files:
        print("  -> No synthetic files found. Output will be same as primary.")
    else:
        for f in synthetic_files:
            try:
                df = pd.read_csv(f)
                df['source'] = 'synthetic_' + os.path.basename(f) # Tagging source
                df_synthetic_list.append(df)
                print(f"  -> Loaded {len(df)} rows from {os.path.basename(f)}")
            except Exception as e:
                print(f"  -> Error loading {f}: {e}")

    # 3. Merge
    if df_synthetic_list:
        df_combined = pd.concat([df_primary] + df_synthetic_list, ignore_index=True)
    else:
        df_combined = df_primary

    # 4. Shuffle (Important for training)
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

    # 5. Save
    print(f"Saving combined dataset to: {OUTPUT_FILE}")
    # We drop the 'source' column before saving because the training script expects specific columns
    # But for debugging, you might want to inspect it before this step.
    # Let's keep strict columns for training compatibility: 'indonesian', 'papua_kokas'
    
    final_cols = ['indonesian', 'papua_kokas']
    if not all(col in df_combined.columns for col in final_cols):
        print("Error: Missing required columns in combined data.")
        return

    df_combined[final_cols].to_csv(OUTPUT_FILE, index=False)
    
    print("=== SUCCESS ===")
    print(f"Total Training Samples: {len(df_combined)}")
    print(f"  - Original: {len(df_primary)}")
    print(f"  - Synthetic: {len(df_combined) - len(df_primary)}")
    print(f"File {OUTPUT_FILE} is ready for training (and is git-ignored).")

if __name__ == "__main__":
    combine_data()
