import pandas as pd
import joblib
import os
from datetime import datetime

# --- Configuration ---
MODEL_PATH = "models/cme_rf_model.joblib"
UNSEEN_DATA_FILE = "data/processed/swis_20250705.csv"  # Change this to the latest preprocessed file
OUTPUT_FILE = "data/predicted/swis_20250705_predicted.csv"
os.makedirs("data/predicted", exist_ok=True)

# --- Load Model ---
print("[INFO] Loading trained model...")
model = joblib.load(MODEL_PATH)

# --- Load Unlabeled SWIS Data ---
df = pd.read_csv(UNSEEN_DATA_FILE, parse_dates=['time'])
print(f"[INFO] Loaded {len(df)} rows from {UNSEEN_DATA_FILE}")

# --- Preprocess Data ---
# Ensure sector columns exist (fill missing ones with 0s)
sector_cols = [f"sector_{i}" for i in range(15, 20)]
for col in sector_cols:
    if col not in df.columns:
        df[col] = 0

df[sector_cols] = df[sector_cols].fillna(0)
df['uncertainty'] = df['uncertainty'].fillna(0)

# Drop rows with missing flux
df = df.dropna(subset=['flux'])

# --- Predict ---
features = ['flux', 'uncertainty'] + sector_cols
X = df[features]
print("[INFO] Predicting CME labels...")
df['CME_Predicted'] = model.predict(X)

# --- Save Output ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"[INFO] Predictions saved to: {OUTPUT_FILE}")
print(df['CME_Predicted'].value_counts())
