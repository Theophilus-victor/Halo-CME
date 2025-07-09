import pandas as pd
import matplotlib.pyplot as plt

# Load tagged data
df = pd.read_csv("data/processed/swis_20250619_tagged.csv", parse_dates=['time'])
df.set_index('time', inplace=True)

# Clean NaN-only columns
df = df.dropna(axis=1, how='all')

# If single row, use scatter plot
single_point = len(df) == 1

plt.figure(figsize=(10, 6))

# Plot each variable
for col in ['flux', 'sector_15', 'sector_16', 'sector_17']:
    if col in df.columns:
        if single_point:
            plt.scatter(df.index, df[col], label=col, s=100)  # Bigger dot
        else:
            plt.plot(df.index, df[col], label=col)

# Highlight CME points
if 'CME' in df.columns:
    cme_times = df[df['CME'] == 1].index
    if not cme_times.empty:
        plt.scatter(cme_times, df.loc[cme_times, 'flux'], color='red', label='Halo CME', zorder=5)

# Improve readability
plt.title("SWIS Flux with Halo CME Annotations")
plt.xlabel("Time")
plt.ylabel("Flux")
plt.legend()

# Adjust axis for single data point
if single_point:
    plt.xlim(df.index[0] - pd.Timedelta(minutes=5), df.index[0] + pd.Timedelta(minutes=5))
    y = df.select_dtypes(include='number').values.flatten()
    y = y[~pd.isnull(y)]
    plt.ylim(min(y)*0.8, max(y)*1.2)

plt.tight_layout()
plt.show()
