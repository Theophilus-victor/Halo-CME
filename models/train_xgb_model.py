import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib
import os

# Load enhanced dataset
df = pd.read_csv("data/processed/swis_all_features.csv", parse_dates=['time'])

# Drop missing values (important for XGBoost)
df = df.dropna(subset=[
    'flux', 'uncertainty', 'sector_15', 'sector_16', 'sector_17', 'sector_18', 'sector_19',
    'flux_diff', 'flux_rolling_mean', 'flux_rolling_std', 'uncertainty_diff',
    'sector_total', 'sector_avg', 'CME'
])

# Feature columns used across entire pipeline
feature_cols = [
    'flux', 'uncertainty',
    'sector_15', 'sector_16', 'sector_17', 'sector_18', 'sector_19',
    'flux_diff', 'flux_rolling_mean', 'flux_rolling_std',
    'uncertainty_diff', 'sector_total', 'sector_avg'
]
X = df[feature_cols]
y = df['CME'].astype(int)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train XGBoost
model = XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("[CONFUSION MATRIX]\n", confusion_matrix(y_test, y_pred))
print("\n[CLASSIFICATION REPORT]\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/cme_xgb_model.joblib")
print("[INFO] XGBoost model saved to: models/cme_xgb_model.joblib")
