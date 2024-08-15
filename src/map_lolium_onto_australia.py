import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

import trims

coord_path = "../reference/coordinates.csv"
phen_path = "../reference/Lolium_glyphosate_cut.csv"

dirname = os.path.dirname(os.path.abspath(__file__))
coord_path = os.path.join(dirname, coord_path)
phen_path = os.path.join(dirname, phen_path)
coord = pd.read_csv(coord_path, index_col=0)
phen = pd.read_csv(phen_path, index_col=0)

trim = trims.dist + trims.outlier + trims.glyphosate
to_drop_coord = [label for label in trim if label in coord.index]
to_drop_phen = [label for label in trim if label in phen.index]
coord = coord.drop(index=to_drop_coord)
phen = phen.drop(index=to_drop_phen)

fig, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(134, 153)
ax.set_ylim(-40, -30)

shapefile_path = "../_deprecated/australia_shapefiles/AUS_2021_AUST_GDA2020.shp"
shapefile_path = os.path.join(dirname, shapefile_path)
gdf = gpd.read_file(shapefile_path)

gdf.plot(ax=ax, color="none", edgecolor="g", linewidth=1)

sns.scatterplot(x=coord["Coordinate_E"], y=coord["Coordinate_N"], hue=phen["glyphosate"], marker="o")
plt.xlabel("Longitude")
plt.ylabel("Lattitude")
plt.title("Glyphosate resistance in SE Australia")

plt.show()
