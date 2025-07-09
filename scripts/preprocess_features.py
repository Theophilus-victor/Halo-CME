import pandas as pd

input_file = "data/processed/swis_all_tagged.csv"
output_file = "data/processed/swis_all_features.csv"

print("[INFO] Loading input file...")
df = pd.read_csv(input_file, parse_dates=['time'])

# Fill missing sector values
sector_cols = [f"sector_{i}" for i in range(15, 20)]
df[sector_cols] = df[sector_cols].fillna(0)

print("[INFO] Creating new feature columns...")

# 1. Flux difference
df['flux_diff'] = df['flux'].diff().fillna(0)

# 2. Uncertainty difference
df['uncertainty_diff'] = df['uncertainty'].diff().fillna(0)

# 3. Sector sum and average
df['sector_total'] = df[sector_cols].sum(axis=1)
df['sector_avg'] = df[sector_cols].mean(axis=1)

# 4. Rolling window stats
df['flux_rolling_mean'] = df['flux'].rolling(window=5, min_periods=1).mean()
df['flux_rolling_std'] = df['flux'].rolling(window=5, min_periods=1).std().fillna(0)

print("[INFO] Saving enhanced feature set...")
df.to_csv(output_file, index=False)
print(f"[INFO] Feature-enhanced file saved to: {output_file}")
