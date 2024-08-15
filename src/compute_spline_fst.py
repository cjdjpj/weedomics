import os
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

chr = "1"
fst_path = "../data/ACC001_vs_ACC041/chr/fst/ACC001_vs_ACC041_chr" + chr + "_fst-fst-1_bp_windows.csv"
fst_output_path = "../data/ACC001_vs_ACC041/chr/fst/chr" + chr + "_spline_fst.csv"
breaks_output_path = "../data/ACC001_vs_ACC041/chr/chr" + chr + "_spline_breaks"
dirname = os.path.dirname(os.path.abspath(__file__))
fst_path = os.path.join(dirname, fst_path)
fst_output_path = os.path.join(dirname, fst_output_path)
breaks_output_path = os.path.join(dirname, breaks_output_path)


### FST
print("----- computing windows from fst -----")
fst = pd.read_csv(fst_path)

pandas2ri.activate()
genwin = importr("GenWin")

r_fst = pandas2ri.py2rpy(fst)

result = genwin.splineAnalyze(
    Y=r_fst[4],
    map=r_fst.rx2("pos_ini"),
    smoothness=10,
    plotRaw=True,
    plotWindows=True,
    method=4
)

window_data_r = result.rx2("windowData")
spline_window_fst = pandas2ri.rpy2py(window_data_r)

### OVERRIDE GenWin mean with manual mean
print("----- computing mean_fst using windows -----")
breaks = result.rx2("breaks").tolist()
breaks = [fst.iloc[0]["pos_ini"]] + list(map(int, breaks))

b = 0
cur_sum = 0
count = 0
new_fst = []
new_count = []

for i in range(len(breaks) - 1):
    start = breaks[i]
    end = breaks[i + 1]

    window = fst[(fst["pos_ini"] >= start) & (fst["pos_ini"] <= end)]
    new_fst.append(window[fst.columns[4]].mean())
    new_count.append(window.shape[0])

last_window = fst[fst["pos_ini"] >= breaks[-1]]
new_fst.append(last_window[fst.columns[4]].mean())
new_count.append(last_window.shape[0])

spline_window_fst["MeanY"] = new_fst
spline_window_fst["SNPcount"] = new_count
spline_window_fst[["WindowStart", "WindowStop"]] = spline_window_fst[["WindowStart", "WindowStop"]].astype(int)

# ## check for inaccurate ones (weird compute by GenWin)
# for index,row in spline_window_fst.iterrows():
#     if abs(row["MeanY"]-new_fst[int(index)-1]) > 1e-12:
#         print(str(row["MeanY"]) + "!=" +  str(new_fst[int(index)-1]))

### WRITE TO CSV
print("----- saving to file -----")
pd.DataFrame(breaks, columns=["breaks"]).to_csv(breaks_output_path, index=False)
spline_window_fst.to_csv(fst_output_path, index=False)
