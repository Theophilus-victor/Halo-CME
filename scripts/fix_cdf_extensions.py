import os

# Folder containing SWIS data
raw_data_dir = "data/raw"

# Rename only files starting with 'AL1_ASW91' and without '.cdf'
for filename in os.listdir(raw_data_dir):
    if filename.startswith("AL1_ASW91") and not filename.lower().endswith(".cdf"):
        old_path = os.path.join(raw_data_dir, filename)
        new_path = old_path + ".cdf"
        os.rename(old_path, new_path)
        print(f"[RENAMED] {filename} -> {os.path.basename(new_path)}")

print("[INFO] CDF file extension fix completed.")
