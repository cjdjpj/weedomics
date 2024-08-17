import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"
phen_path = "../reference/Lolium_glyphosate_cut.csv"
chr = "Genome-wide"
df = utils.create_df(distances_path, fst_path, trims.dist + trims.glyphosate + trims.outlier)

dirname = os.path.dirname(os.path.abspath(__file__))
phen_path = os.path.join(dirname, phen_path)
phen = pd.read_csv(phen_path, index_col = 0)

phen_matrix = [[abs(i-j) for j in phen['glyphosate']] for i in phen['glyphosate']]

phen_matrix = pd.DataFrame(phen_matrix, index = phen["glyphosate"].index, columns = phen["glyphosate"].index)
flattened_phen_matrix = utils.trim_df(phen_matrix, trims.dist + trims.outlier + trims.glyphosate)
flattened_phen_matrix = utils.flatten_df(phen_matrix)
df["glyphosate"] = flattened_phen_matrix["data"]

match chr:
    case "Chr1":
        cluster1_threshold = 0.01087
        cluster2_threshold = 0.015
    case "Chr2":
        cluster1_threshold = 0.01083
        cluster2_threshold = 0.0142
    case "Chr3":
        cluster1_threshold = 0.0103
        cluster2_threshold = 0.0142
    case "Chr4":
        cluster1_threshold = 0.0097
        cluster2_threshold = 0.0142
    case "Chr5":
        cluster1_threshold = 0.0117
        cluster2_threshold = 0.0154
    case "Chr6":
        cluster1_threshold = 0.0105
        cluster2_threshold = 0.0154
    case "Chr7":
        cluster1_threshold = 0.0099
        cluster2_threshold = 0.0145
    case "Genome-wide":
        cluster1_threshold = 0.0115
        cluster2_threshold = 0.016

cluster1 = df[df["fst"] < cluster1_threshold]
cluster2 = df[(df["fst"] >= cluster1_threshold) & (df["fst"] < cluster2_threshold)]
cluster3 = df[df["fst"] >= cluster2_threshold]

slope, intercept, r_value, p_value, std_err = linregress(cluster1["distances"], cluster1["fst"])

plt.figure(figsize = (9,9))
plt.xlabel("Distance (km)")
plt.ylabel("fst")
plt.title("Geographical distance vs fst with glyphosate resistance as hue (" + chr + ")")

df = df.sort_values("glyphosate")
sns.scatterplot(x = df["distances"], y = df["fst"], hue = df["glyphosate"], linewidth = 0)
sns.lineplot(x=[df["distances"].min(), df["distances"].max()], y=[df["distances"].min() * slope + intercept, df["distances"].max() * slope + intercept], color="red")

plt.text(plt.gca().get_xlim()[0] + 0.87 * (plt.gca().get_xlim()[1]-plt.gca().get_xlim()[0]),
         plt.gca().get_ylim()[0] + 0.04 * (plt.gca().get_ylim()[1]-plt.gca().get_ylim()[0]),
         "Glyphosate resistance\npercent difference\nbetween pools",
         fontsize=8,
         ha="right",
         va="center")

print("Slope:", slope)
print("Intercept:", intercept)
print("r^2:", r_value**2)
print("p-value:", p_value)
print("Standard error:", std_err)

plt.show()
