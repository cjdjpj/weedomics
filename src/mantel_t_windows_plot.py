import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

mantel_path = "../data/all_pools/ws10000/mantel_results_twotail.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
mantel_path = os.path.join(dirname, mantel_path)
mantel_results = pd.read_csv(mantel_path, index_col = 0)

plt.figure(figsize = (9,9))
sns.histplot(mantel_results["Mantel_p"], bins=50)

sorted_mantel = mantel_results.sort_values("Mantel_p")

p_threshold = sorted_mantel["Mantel_p"].quantile(0.95)
print(p_threshold)
uncorrelated_windows = mantel_results[mantel_results["Mantel_p"] > p_threshold]
print(uncorrelated_windows)

pd.set_option("display.max_rows", None)
print(sorted_mantel)

plt.figure(figsize = (30,10))
plt.title("Mantel test across windows (FST vs geographic distance)(two-tailed)")
plt.ylabel("p-value")
plt.xticks(rotation=90, fontsize=7)
sns.barplot(sorted_mantel["Mantel_p"])
plt.show()
