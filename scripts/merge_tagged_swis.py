import os
import pandas as pd
from glob import glob

# Set folder path
processed_folder = "data/processed"
output_file = "data/processed/swis_all_tagged.csv"

# Find all tagged files
csv_files = glob(os.path.join(processed_folder, "swis_*_tagged.csv"))
print(f"[INFO] Found {len(csv_files)} tagged files.")

# List to hold valid DataFrames
all_dfs = []

# Loop through files
for file in csv_files:
    if os.path.getsize(file) == 0:
        print(f"[WARNING] Skipping empty file: {file}")
        continue
    try:
        df = pd.read_csv(file, parse_dates=['time'])
        df['source_file'] = os.path.basename(file)
        all_dfs.append(df)
    except pd.errors.EmptyDataError:
        print(f"[ERROR] EmptyDataError in file: {file}")
        continue
    except Exception as e:
        print(f"[ERROR] Failed to load {file}: {e}")
        continue

# Concatenate all valid DataFrames
if all_dfs:
    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df = full_df.dropna(subset=['flux', 'CME'])

    # Save merged file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    full_df.to_csv(output_file, index=False)
    print(f"[INFO] Merged file saved to: {output_file}")
    print(f"[INFO] Total merged rows: {len(full_df)}")
    print(f"[INFO] CME-labeled points: {full_df['CME'].sum()}")
else:
    print("[ERROR] No valid dataframes to merge.")
