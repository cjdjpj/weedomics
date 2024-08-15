import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sum_stats = "fst"
spline_path = "../data/ACC001_vs_ACC041/spline_" + sum_stats + ".csv"

dirname = os.path.dirname(os.path.abspath(__file__))
spline_path = os.path.join(dirname, spline_path)
spline = pd.read_csv(spline_path)

spline = spline[spline["SNPcount"] > 30]

epsilon = 1e-12
def approximately_equal(value, target, epsilon):
    return abs(value - target) < epsilon

if sum_stats == "fst":
    mask = ~(
        spline["MeanY"].apply(lambda x: approximately_equal(x, 1.0, epsilon)) |
        spline["MeanY"].apply(lambda x: approximately_equal(x, 0.666666666666, epsilon)) |
        spline["MeanY"].apply(lambda x: approximately_equal(x, 0.333333333333, epsilon)) |
        spline["MeanY"].apply(lambda x: approximately_equal(x, 0.5, epsilon))
    )

    spline = spline[mask]

plt.figure(figsize=(9,9))
plt.title("Smooth spline " + sum_stats + " across genome")
plt.xlabel("Position on genome")
plt.ylabel(sum_stats)
plt.xticks([])
sns.scatterplot(x=spline.index, y=spline["MeanY"], hue=spline["chr"], palette='coolwarm', edgecolor = None)
plt.show()
# plt.savefig(sum_stats + ".png", dpi=300)
