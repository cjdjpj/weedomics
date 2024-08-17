import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

import utils
import trims

distances_path = "../reference/orthodromic_distance.csv"
fst_path = "../data/all_pools/genome_mean_fst.csv"
chr = "Genome-wide"
df = utils.create_df(distances_path, fst_path, trims.dist)

plt.figure(figsize = (9,9))
plt.xlabel("Distance (km)")
plt.ylabel("Fst")
plt.title("Geographical distance vs fst linreg (" + chr + ")")
sns.scatterplot(x = df["distances"], y = df["fst"])

slope, intercept, r_value, p_value, std_err = linregress(df["distances"], df["fst"])

sns.lineplot(x=[df["distances"].min(), df["distances"].max()], y=[df["distances"].min() * slope + intercept, df["distances"].max() * slope + intercept], color="red")
print("Slope:", slope)
print("Intercept:", intercept)
print("r^2:", r_value**2)
print("p-value:", p_value)
print("Standard error:", std_err)

plt.show()
