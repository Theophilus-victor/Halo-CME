import pandas as pd
import joblib
import os

# === Config ===
input_file = "data/processed/swis_all_features.csv"  # Feature-enhanced dataset
model_path = "models/cme_xgb_model.joblib"            # Trained XGBoost model
output_file = "data/processed/swis_predictions.csv"   # Output with predictions

# === Load Data ===
print("[INFO] Loading feature-enhanced SWIS data...")
df = pd.read_csv(input_file, parse_dates=["time"])
df = df.dropna()  # Clean NaNs if any

# === Load Model ===
print("[INFO] Loading trained model...")
model = joblib.load(model_path)

# === Prepare Features ===
feature_cols = [
    'flux', 'uncertainty', 'sector_15', 'sector_16', 'sector_17',
    'sector_18', 'sector_19', 'flux_rolling_mean', 'flux_rolling_std',
    'flux_diff', 'uncertainty_diff', 'sector_total', 'sector_avg'
]

X = df[feature_cols]

# === Make Predictions ===
print("[INFO] Making predictions...")
df['CME_Predicted'] = model.predict(X)

# === Save Predictions ===
os.makedirs("data/processed", exist_ok=True)
df.to_csv(output_file, index=False)
print(f"[INFO] Predictions saved to: {output_file}")

# === Summary ===
total = len(df)
positives = df['CME_Predicted'].sum()
print(f"\n[SUMMARY] Total Points: {total} | Predicted Halo CME Events: {int(positives)}")
