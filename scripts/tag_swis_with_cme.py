import pandas as pd
from datetime import datetime

# --- Load SWIS Data ---
swis_path = 'data/processed/swis_20250619_tagged.csv'
swis_df = pd.read_csv(swis_path, parse_dates=['time'])
swis_df.set_index('time', inplace=True)

# --- Load Halo CME Time Windows ---
halo_path = 'data/raw/cactus_halo_cme.csv'
halo_df = pd.read_csv(halo_path, parse_dates=['start_time', 'end_time'])

# --- Initialize CME Tag ---
swis_df['CME'] = 0

# --- Tag SWIS Points Within Any CME Window ---
for idx, row in halo_df.iterrows():
    mask = (swis_df.index >= row['start_time']) & (swis_df.index <= row['end_time'])
    swis_df.loc[mask, 'CME'] = 1

# --- Save Tagged Data ---
swis_df.to_csv('data/processed/swis_20250619_tagged.csv')
print(f"[INFO] Tagged SWIS data saved: data/processed/swis_20250619_tagged.csv")

# --- Quick Stats ---
print(f"\n[SUMMARY] Total Points: {len(swis_df)} | CME Points: {swis_df['CME'].sum()}")
