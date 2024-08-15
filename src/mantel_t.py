import mantel

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"
chr = "Genome-wide"
df = utils.create_df(distances_path, fst_path, trims.dist + trims.outlier)

result = mantel.test(df["distances"], df["fst"], tail="two-tail")
print(result)

fig, axis = mantel.plot(result)
# fig.savefig("mantel.svg")
