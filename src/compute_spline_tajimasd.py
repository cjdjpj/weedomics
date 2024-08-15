import os
import pandas as pd

chr = "1"
tajimasd_pool = "ACC041" # pool to compute tajimasd for
tajimasd_path = "../data/ACC001_vs_ACC041/chr/tajimasd/ACC001_vs_ACC041_chr" + chr + "_tajimasd.csv"
breaks_path = "../data/ACC001_vs_ACC041/chr/chr" + chr + "_spline_breaks"
tajimasd_output_path = "../data/ACC001_vs_ACC041/chr/tajimasd/chr" + chr + "_spline_tajimasd_" + tajimasd_pool + ".csv"
dirname = os.path.dirname(os.path.abspath(__file__))
tajimasd_path = os.path.join(dirname, tajimasd_path)
breaks_path = os.path.join(dirname, breaks_path)
tajimasd_output_path = os.path.join(dirname, tajimasd_output_path)

### TAJIMAS_D PROCESSING
print("----- reading in tajimasd and breaks  -----")
tajimasd = pd.read_csv(tajimasd_path).transpose()
breaks = pd.read_csv(breaks_path)["breaks"].tolist()

pools = tajimasd.loc["Pool",:].to_list()

tajimasd = tajimasd.iloc[2:,:]
tajimasd.index = tajimasd.index.to_series().apply(lambda x: x.split("_")[2])
tajimasd = tajimasd.reset_index()

tajimasd.columns = ["pos_ini"] + pools
tajimasd[tajimasd.columns[0]] = tajimasd[tajimasd.columns[0]].astype(int)
tajimasd[tajimasd.columns[1]] = tajimasd[tajimasd.columns[1]].astype(float)
tajimasd[tajimasd.columns[2]] = tajimasd[tajimasd.columns[2]].astype(float)

### TAJIMAS_D WITH SAME WINDOWS
print("----- computing mean_tajimasd using windows -----")
b = 0
cur_sum = 0
count = 0
new_tajimasd = []
new_count = []

for i in range(len(breaks) - 1):
    start = breaks[i]
    end = breaks[i + 1]

    window = tajimasd[(tajimasd["pos_ini"] >= start) & (tajimasd["pos_ini"] <= end)]
    new_tajimasd.append(window[tajimasd_pool].mean())
    new_count.append(window.shape[0])

last_window = tajimasd[tajimasd["pos_ini"] >= breaks[-1]]
new_tajimasd.append(last_window[tajimasd_pool].mean())
new_count.append(last_window.shape[0])

spline_window_tajimasd = pd.DataFrame({
    "WindowStart": breaks,
    "MeanY": new_tajimasd,
    "SNPcount": new_count,
})
print("----- saving to file -----")
spline_window_tajimasd.to_csv(tajimasd_output_path, index=False)
