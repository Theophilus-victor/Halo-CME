import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Halo CME Predictor", layout="wide")

st.title("☀️ Halo CME Prediction Dashboard")

# Load enhanced SWIS data
df = pd.read_csv("data/processed/swis_all_features.csv", parse_dates=['time'])

st.markdown(f"📊 **Total Rows:** {len(df):,}")

# Drop rows with missing values in prediction features
feature_cols = [
    'flux', 'uncertainty',
    'sector_15', 'sector_16', 'sector_17', 'sector_18', 'sector_19',
    'flux_diff', 'flux_rolling_mean', 'flux_rolling_std',
    'uncertainty_diff', 'sector_total', 'sector_avg'
]
df = df.dropna(subset=feature_cols)

# Load trained model
model = joblib.load("models/cme_xgb_model.joblib")

# Predict
X = df[feature_cols]
df['CME_Predicted'] = model.predict(X)

# Summary
st.markdown(f"🌪️ **Predicted Halo CME Events:** {df['CME_Predicted'].sum():,}")

# Display data
st.dataframe(df[['time', 'flux', 'CME_Predicted']].tail(50), use_container_width=True)
