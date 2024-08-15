import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

variances_path = "../_deprecated/1indiv-cov-breadth/variances.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
variances_path = os.path.join(dirname, variances_path)
variances = pd.read_csv(variances_path, header=None)

plt.figure(figsize=(9, 9))
plt.xlabel("Window size")
plt.ylabel("Variance (log)")
plt.yscale("log")
plt.title("Variance of heterozygosity across windows")
sns.scatterplot(x=variances.iloc[:, 0], y=variances.iloc[:, 1], edgecolor=None)
plt.show()

