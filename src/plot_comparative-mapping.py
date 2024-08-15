import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

mapping_path = "../data/all_pools/mapping.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
mapping_path = os.path.join(dirname, mapping_path)
comp_map = pd.read_csv(mapping_path)
comp_map["Percent_properly_paired"] = comp_map["Percent_properly_paired"].map(lambda x: 100 * x)

plt.figure(figsize = (9,9))
plt.title("Comparative mapping of pools of interest to Lolium Rigidum and Perenne ref genomes")
plt.ylabel("Percent properly paired (%)")
plt.xlabel("ClusterNumber-PoolName")
plt.ylim(70, 100)
ax = sns.barplot(x=comp_map["#cluster-Pool_name"], y=comp_map["Percent_properly_paired"], hue = comp_map["Species"])
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha="center", va="center", 
                xytext=(0, 9), 
                textcoords="offset points",
                fontsize = 8
                )
plt.show()
