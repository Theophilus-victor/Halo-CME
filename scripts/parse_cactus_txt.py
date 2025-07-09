import pandas as pd
from datetime import datetime, timedelta

# --- Input / Output paths ---
input_file = 'data/cactus/cme_qkl.txt'
output_file = 'data/raw/cactus_halo_cme.csv'

start_times = []
end_times = []
durations = []

with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue  # Skip headers and separators

        parts = line.split("|")
        if len(parts) < 10:
            continue  # Skip malformed lines

        t0 = parts[1].strip()
        dt0 = parts[2].strip()
        halo_flag = parts[-1].strip()

        # Check for halo CME indication (II, III, or IV)
        if halo_flag in ("II", "III", "IV"):
            try:
                start_time = datetime.strptime(t0, "%Y/%m/%d %H:%M")
                duration = int(dt0)
                end_time = start_time + timedelta(hours=duration)

                start_times.append(start_time)
                end_times.append(end_time)
                durations.append(duration)
            except Exception as e:
                print(f"[WARN] Skipping due to error: {e}\nLine: {line}")

# --- Create DataFrame and Save ---
df = pd.DataFrame({
    'start_time': start_times,
    'end_time': end_times,
    'duration_hr': durations
})

df.to_csv(output_file, index=False)
print(f"[INFO] Parsed halo CMEs saved to: {output_file}")
