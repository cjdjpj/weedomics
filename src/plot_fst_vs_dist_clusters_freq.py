import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"
chr = "Genome-wide"
cluster_examined = 3
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

pool_counts = {}
for pair in clusters[cluster_examined-1]["pool_pairs"]:
    pool1, pool2 = pair
    pool_counts[pool1] = pool_counts.get(pool1, 0) + 1
    pool_counts[pool2] = pool_counts.get(pool2, 0) + 1

n = len(pool_counts)
for key in pool_counts:
    pool_counts[key] /= n-1

frequencies = pd.DataFrame({"pool": list(pool_counts.keys()), "frequency": list(pool_counts.values())}).sort_values(by="pool")

plt.figure(figsize=(18,9))
plt.xticks(rotation=90, fontsize = 7)
plt.title("Frequency of pools occurance in cluster " + str(cluster_examined))
plt.xlabel("Pool")
plt.ylabel("Frequency")
sns.barplot(x = frequencies["pool"], y = frequencies["frequency"], color = sns.color_palette()[cluster_examined-1])
sns.lineplot(x = range(0, n), y = len(clusters[cluster_examined-1])/len(df), color = "red", linestyle = "--")
plt.show()

