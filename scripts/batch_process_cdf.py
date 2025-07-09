import os
import glob
from spacepy import pycdf
import pandas as pd
from cdflib import CDF, cdfepoch
import numpy as np


raw_dir = "data/raw"
output_dir = "data/processed"

os.makedirs(output_dir, exist_ok=True)

# Find all .cdf files
cdf_files = glob.glob(os.path.join(raw_dir, "*.cdf"))
print(f"[INFO] Found {len(cdf_files)} CDF files to process.")
# Inside batch_process_cdf.py (after detecting files)
def process_cdf_file(filepath):
    try:
        cdf = CDF(filepath)

        epoch = cdf['epoch_for_cdf_mod']
        time = pd.to_datetime(cdfepoch.to_datetime(epoch))

        def extract(name):
            try:
                return np.nanmean(np.squeeze(cdf[name]), axis=1)
            except:
                return np.full(len(time), np.nan)

        df = pd.DataFrame({
            'time': time,
            'flux': extract('integrated_flux_mod'),
            'uncertainty': extract('flux_uncer'),
            'sector_15': extract('integrated_flux_s15_mod'),
            'sector_16': extract('integrated_flux_s16_mod'),
            'sector_17': extract('integrated_flux_s17_mod'),
            'sector_18': extract('integrated_flux_s18_mod'),
            'sector_19': extract('integrated_flux_s19_mod'),
        })

        date_str = pd.to_datetime(time[0]).strftime("%Y%m%d")
        output_path = os.path.join(output_dir, f"swis_{date_str}_tagged.csv")
        df.to_csv(output_path, index=False)
        print(f"[SAVED] {output_path}")

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

# Process all files
for cdf_file in cdf_files:
    process_cdf_file(cdf_file)
