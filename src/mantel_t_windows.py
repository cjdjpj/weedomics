import os
import pandas as pd
import mantel

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/ws10000/genome_fst-fst-10000_bp_windows.csv"
output_path = "../data/all_pools/ws10000/mantel_results_twotail.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
fst_path = os.path.join(dirname, fst_path)
fst = pd.read_csv(fst_path, index_col = 0)
distances_path = os.path.join(dirname, distances_path)
distances = pd.read_csv(distances_path, index_col = 0)

mantel_results = []

num_pools = 167
num_windows = fst.shape[0]

distances = utils.trim_df(distances, trims.dist + trims.outlier)

fst.index = fst.index.astype(str) + "_" + fst["pos_ini"].astype(str) + "_" + fst["pos_fin"].astype(str)

fst = fst.drop(["pos_ini", "pos_fin"], axis=1)

pd.set_option("display.max_rows", None)  # None means unlimited
print(fst)

labels = []
for pool in range(num_pools):
    pool_name = fst.columns[pool].split("_", maxsplit=2)[2]
    labels.append(pool_name)

for row, window in fst.iterrows():
    fst_matrix = []
    for col in range(num_pools):
        matrix_row = window.iloc[col*num_pools : col*num_pools+num_pools].tolist()

        fst_matrix.append(matrix_row)

    fst_matrix = pd.DataFrame(fst_matrix, index=labels, columns=labels)
    fst_matrix = utils.trim_df(fst_matrix, trims.dist + trims.outlier)

    mantel_results.append(mantel.test(fst_matrix,distances, tail="two-tail"))


output_path = os.path.join(dirname, output_path)
file = open(output_path,"w")

file.write("WindowName,Mantel_r,Mantel_p,Mantel_z,Mantel_mean,Mantel_std\n")
for i in range(num_windows):
    file.write(fst.index[i] + "," + 
        str(mantel_results[i].r) + "," + 
        str(mantel_results[i].p) + "," + 
        str(mantel_results[i].z) + "," +
        str(mantel_results[i].mean) + "," + 
        str(mantel_results[i].std) + "\n")

