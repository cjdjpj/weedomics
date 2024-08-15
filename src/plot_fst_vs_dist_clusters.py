import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"
chr = "Genome-wide"
df = utils.create_df(distances_path, fst_path, trims.dist)

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
clusters = [cluster1, cluster2, cluster3]

plt.figure(figsize = (9,9))
plt.xlabel("Distance (km)")
plt.ylabel("Fst")
plt.title("Geographical distance vs fst clustered linreg (" + chr + ")")
for cluster in clusters:
    sns.scatterplot(x = cluster["distances"], y = cluster["fst"], s=15)

slope, intercept, r_value, p_value, std_err = linregress(cluster1["distances"], cluster1["fst"])

sns.lineplot(x=[df["distances"].min(), df["distances"].max()], y=[df["distances"].min() * slope + intercept, df["distances"].max() * slope + intercept], color="red")
print("Slope:", slope)
print("Intercept:", intercept)
print("r^2:", r_value**2)
print("p-value:", p_value)
print("Standard error:", std_err)

plt.show()
