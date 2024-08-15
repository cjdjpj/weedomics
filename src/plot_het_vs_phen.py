import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

import trims
import utils

heterozygosity_path = "../data/all_pools/ws10000/genome_10000_het.csv"
phen_path = "../reference/Lolium_glyphosate_cut.csv"
chr = "Genome-wide"

dirname = os.path.dirname(os.path.abspath(__file__))
phen_path = os.path.join(dirname, phen_path)
heterozygosity_path = os.path.join(dirname, heterozygosity_path)
phen = pd.read_csv(phen_path, index_col = 0)
heterozygosity = pd.read_csv(heterozygosity_path, index_col = 0)

trim = trims.dist + trims.outlier + trims.glyphosate
heterozygosity = utils.trim_df(heterozygosity, trim)
phen = utils.trim_df(phen, trim)

### ONLY KEEP NON-0 GLYPHOSATE RESISTANCE
kept_pools = phen[phen['glyphosate'] >= 1e-9].index
phen = phen.loc[kept_pools]
heterozygosity = heterozygosity.loc[kept_pools]

slope, intercept, r_value, p_value, std_err = linregress(phen["glyphosate"], heterozygosity["Mean_across_windows"])

plt.figure(figsize = (9,9))
sns.scatterplot(x=phen["glyphosate"], y=heterozygosity["Mean_across_windows"])
plt.xlabel("Glyphostate resistance (%)")
plt.ylabel("Heterozygosity ($\Theta_\pi = 4N_e\mu$)")
plt.title("Glyphosate resistance vs mean heterozygosity across windows")

sns.lineplot(x=[phen["glyphosate"].min(), phen["glyphosate"].max()], y=[phen["glyphosate"].min() * slope + intercept, phen["glyphosate"].max() * slope + intercept], color="red")
print("Slope:", slope)
print("Intercept:", intercept)
print("r:", r_value)
print("p-value:", p_value)
print("Standard error:", std_err)

plt.show()
