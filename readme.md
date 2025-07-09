[.cdf]     -->  parsed →  swis_YYYYMMDD.csv
[.txt]     -->  filtered → cactus_halo_cme.csv
                     |
swis + cactus → tag_swis_with_cme.py → swis_YYYYMMDD_tagged.csv
python scripts/fix_cdf_extensions.py
python scripts/batch_process_cdf.py
python scripts/tag_swis_with_cme.py
python scripts/merge_tagged_swis.py
python scripts/train_cme_model.py
