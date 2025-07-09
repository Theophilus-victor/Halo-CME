import os
import pandas as pd
from datetime import datetime
from glob import glob

# --- Load halo CME start dates ---
halo_df = pd.read_csv("data/raw/cactus_halo_cme.csv", parse_dates=['start_time'])
halo_dates = halo_df['start_time'].dt.strftime('%Y%m%d').unique()

# --- Scan your raw data folder ---
cdf_files = glob("data/raw/*.cdf")
cdf_dates = [os.path.basename(f).split('_')[4] for f in cdf_files if "_" in f]

# --- Check which halo CME dates are missing in CDFs ---
missing_dates = sorted(set(halo_dates) - set(cdf_dates))

# --- Output results ---
print(f"[INFO] Halo CME Dates with no matching CDF file: {len(missing_dates)}")
for d in missing_dates:
    print(d)

# Optional: save to file
with open("missing_cme_swis_dates.txt", "w") as f:
    for d in missing_dates:
        f.write(d + '\n')

print("\n[INFO] Saved missing date list to: missing_cme_swis_dates.txt")
