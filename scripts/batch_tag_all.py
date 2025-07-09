# scripts/batch_tag_all.py

from glob import glob
import os

input_folder = 'data/processed'
for file in glob(f"{input_folder}/swis_*.csv"):
    date_str = os.path.basename(file).split('_')[1].split('.')[0]
    tagged_file = f"{input_folder}/swis_{date_str}_tagged.csv"
    os.system(f"python scripts/tag_swis_with_cme.py --date {date_str}")
