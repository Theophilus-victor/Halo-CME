import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# Configuration
INPUT_CSV = "data/processed/swis_20250619_tagged.csv"
OUTPUT_X = "data/processed/X_windows.npy"
OUTPUT_Y = "data/processed/y_labels.npy"
WINDOW_SIZE = 60  # Number of time steps per window
STEP = 1           # How much to move the window each time

# Feature columns from particle data
FEATURE_COLS = ['flux', 'sector_15', 'sector_16', 'sector_17', 'sector_18', 'sector_19']
LABEL_COL = 'CME'

def generate_sliding_windows():
    print(f"[INFO] Loading: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV, parse_dates=['time'])

    # Drop rows with missing values in any feature column
    df.dropna(subset=FEATURE_COLS + [LABEL_COL], inplace=True)

    # Normalize features
    scaler = MinMaxScaler()
    df.dropna(subset=[LABEL_COL], inplace=True)
    df[FEATURE_COLS] = df[FEATURE_COLS].fillna(0)

    df.set_index("time", inplace=True)

    X, y = [], []

    for i in range(0, len(df) - WINDOW_SIZE, STEP):
        window = df.iloc[i:i + WINDOW_SIZE]
        label = int(df[LABEL_COL].iloc[i + WINDOW_SIZE - 1])  # Label based on end of window
        X.append(window[FEATURE_COLS].values)
        y.append(label)

    X = np.array(X)
    y = np.array(y)

    print(f"[INFO] Total Samples: {len(X)}")
    print(f"[INFO] X shape: {X.shape} | y shape: {y.shape}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_X), exist_ok=True)

    # Save as .npy files
    np.save(OUTPUT_X, X)
    np.save(OUTPUT_Y, y)
    print(f"[INFO] Saved X to: {OUTPUT_X}")
    print(f"[INFO] Saved y to: {OUTPUT_Y}")

if __name__ == "__main__":
    generate_sliding_windows()
