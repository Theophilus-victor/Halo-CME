import pandas as pd
from pathlib import Path

# Input CACTUS CSV (already parsed from .txt earlier)
input_file = "data/raw/cactus_halo_cme.csv"
output_file = "halo_cme_dates.txt"

# Load CSV
df = pd.read_csv(input_file, parse_dates=['start_time'])

# Extract just the date part (YYYY-MM-DD) where CME is halo-labeled
halo_dates = df['start_time'].dt.strftime('%Y-%m-%d').dropna().unique()
halo_dates = sorted(halo_dates)

# Save to file
with open(output_file, 'w') as f:
    for d in halo_dates:
        f.write(d + '\n')

# Print summary
print(f"[INFO] Total unique Halo CME dates: {len(halo_dates)}")
print("[INFO] Sample:")
print("\n".join(halo_dates[:10]), "...\n")
print(f"[INFO] Saved list to: {output_file}")
