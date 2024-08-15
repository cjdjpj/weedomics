import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import utils
import trims

heterozygosity_path = "../data/all_pools/ws10000/genome_10000_het.csv"
chr = "Genome-wide"

dirname = os.path.dirname(os.path.abspath(__file__))
heterozygosity_path = os.path.join(dirname, heterozygosity_path)
heterozygosity = pd.read_csv(heterozygosity_path, index_col = 0)
heterozygosity = utils.trim_df(heterozygosity, trims.outlier)

het_mean = heterozygosity.iloc[:, 0]
het_windows = heterozygosity.iloc[:, 1:]

for row_label in het_windows.index:
    for col_label in het_windows.columns:
        if het_windows.at[row_label, col_label] > 0.3:
            print(f"{row_label}, {col_label} = {het_windows.at[row_label, col_label]}")

plt.figure(figsize = (9,9))
plt.xlabel("Pools")
plt.ylabel("Windows")
plt.title("Heterozygosity ($\Theta_\pi = 4N_e\mu$) (" + chr + ")")

sns.heatmap(het_windows)
plt.show()
