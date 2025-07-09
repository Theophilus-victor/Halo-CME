import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib

# === 1. Load dataset ===
input_file = "data/processed/swis_all_tagged.csv"
df = pd.read_csv(input_file, parse_dates=['time'])

# === 2. Basic cleanup ===
df = df.dropna(subset=['flux', 'CME'])  # Drop rows with missing target or critical feature

# Fill missing sector values with 0
sector_cols = [f"sector_{i}" for i in range(15, 20)]
df[sector_cols] = df[sector_cols].fillna(0)

# === 3. Prepare features and target ===
feature_cols = ['flux', 'uncertainty'] + sector_cols
X = df[feature_cols]
y = df['CME'].astype(int)

# === 4. Split dataset ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === 5. Handle imbalance with SMOTE ===
# Fill any leftover NaNs in training set to ensure compatibility with SMOTE
X_train = X_train.fillna(0)
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# === 6. Train model ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_res, y_train_res)

# === 7. Evaluate ===
y_pred = model.predict(X_test)
print("[CONFUSION MATRIX]\n", confusion_matrix(y_test, y_pred))
print("\n[CLASSIFICATION REPORT]\n", classification_report(y_test, y_pred))

# === 8. Save the model ===
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/cme_rf_model.joblib")
print("[INFO] Model saved to: models/cme_rf_model.joblib")

# === 9. Class distribution summary ===
print(df['CME'].value_counts())
