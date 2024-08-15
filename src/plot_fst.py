import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import utils
import trims

fst_path = "../data/all_pools/genome_mean_fst.csv"
chr = "Genome-wide"

dirname = os.path.dirname(os.path.abspath(__file__))
fst_path = os.path.join(dirname, fst_path)
fst = pd.read_csv(fst_path, index_col = 0)
fst = utils.trim_df(fst, trims.outlier)

plt.figure(figsize = (9,9))
plt.xlabel("Pools")
plt.ylabel("Pools")
plt.title("Fst (" + chr + ")")

sns.heatmap(fst)
plt.show()
