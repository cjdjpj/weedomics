import os
import pandas as pd

chr = "1"
theta_pool = "ACC001" # pool to compute theta for
theta_path = "../data/ACC001_vs_ACC041/chr/theta/ACC001_vs_ACC041_chr" + chr + "_theta.csv"
breaks_path = "../data/ACC001_vs_ACC041/chr/chr" + chr + "_spline_breaks"
theta_output_path = "../data/ACC001_vs_ACC041/chr/theta/chr" + chr + "_spline_theta" + theta_pool + ".csv"
dirname = os.path.dirname(os.path.abspath(__file__))
theta_path = os.path.join(dirname, theta_path)
breaks_path = os.path.join(dirname, breaks_path)
theta_output_path = os.path.join(dirname, theta_output_path)

### THETA PROCESSING
print("----- reading in theta and breaks  -----")
theta = pd.read_csv(theta_path).transpose()
breaks = pd.read_csv(breaks_path)["breaks"].tolist()

pools = theta.loc["Pool",:].to_list()

theta = theta.iloc[2:,:]
theta.index = theta.index.to_series().apply(lambda x: x.split("_")[2])
theta = theta.reset_index()

theta.columns = ["pos_ini"] + pools
theta[theta.columns[0]] = theta[theta.columns[0]].astype(int)
theta[theta.columns[1]] = theta[theta.columns[1]].astype(float)
theta[theta.columns[2]] = theta[theta.columns[2]].astype(float)

### THETA WITH SAME WINDOWS
print("----- computing mean_theta using windows -----")
b = 0
cur_sum = 0
count = 0
new_theta = []
new_count = []

for i in range(len(breaks) - 1):
    start = breaks[i]
    end = breaks[i + 1]

    window = theta[(theta["pos_ini"] >= start) & (theta["pos_ini"] <= end)]
    new_theta.append(window[theta_pool].mean())
    new_count.append(window.shape[0])

last_window = theta[theta["pos_ini"] >= breaks[-1]]
new_theta.append(last_window[theta_pool].mean())
new_count.append(last_window.shape[0])

spline_window_theta = pd.DataFrame({
    "WindowStart": breaks,
    "MeanY": new_theta,
    "SNPcount": new_count,
})
print("----- saving to file -----")
spline_window_theta.to_csv(theta_output_path, index=False)
