import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
fst_path = os.path.join(dirname, fst_path)
distances_path = os.path.join(dirname, distances_path)
fst = pd.read_csv(fst_path, index_col = 0)
distances = pd.read_csv(distances_path, index_col = 0)

fst = utils.trim_df(fst, trims.outlier + trims.dist)
distances = utils.trim_df(distances, trims.outlier + trims.dist)

sns.clustermap(distances)
# sns.clustermap(fst)

plt.savefig("dendrogram_dist.png", dpi=300)
plt.show()
