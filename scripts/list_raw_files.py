import os

raw_data_dir = "data/raw"

print("[INFO] Listing files in data/raw:")
for f in os.listdir(raw_data_dir):
    print("   ", f)
