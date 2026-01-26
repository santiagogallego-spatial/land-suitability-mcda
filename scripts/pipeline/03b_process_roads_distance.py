import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import numpy as np
from scipy.ndimage import distance_transform_edt
from pathlib import Path

# =============================
# PATHS
# =============================
ROADS = Path("data/processed/roads.gpkg")
BASE_GRID = Path("data/processed/base_grid.tif")

OUT_RASTER = Path("data/processed/roads_distance.tif")
OUT_NORM = Path("data/processed/roads_distance_norm.tif")

OUT_RASTER.parent.mkdir(parents=True, exist_ok=True)

# =============================
# PARAMETERS
# =============================
MAX_DISTANCE = 10000  # metros (10 km)

# =============================
# LOAD BASE GRID
# =============================
with rasterio.open(BASE_GRID) as ref:
    meta = ref.meta.copy()
    transform = ref.transform
    shape = (ref.height, ref.width)
    crs = ref.crs

# =============================
# LOAD ROADS
# =============================
roads = gpd.read_file(ROADS).to_crs(crs)

if roads.empty:
    raise RuntimeError("❌ Roads layer is empty")

# =============================
# RASTERIZE ROADS
# =============================
road_raster = rasterize(
    [(geom, 1) for geom in roads.geometry],
    out_shape=shape,
    transform=transform,
    fill=0,
    dtype="uint8"
)

# =============================
# DISTANCE TRANSFORM
# =============================
# distance_transform_edt calcula distancia a los ceros,
# por eso invertimos
distance = distance_transform_edt(1 - road_raster)

# convertir de píxeles a metros
pixel_size = transform.a
distance_m = distance * pixel_size

# limitar distancia máxima
distance_m = np.clip(distance_m, 0, MAX_DISTANCE)

# =============================
# SAVE DISTANCE RASTER
# =============================
meta.update(dtype="float32", count=1)

with rasterio.open(OUT_RASTER, "w", **meta) as dst:
    dst.write(distance_m.astype("float32"), 1)

# =============================
# NORMALIZATION (0–1, closer = better)
# =============================
norm = 1 - (distance_m / MAX_DISTANCE)
norm = np.clip(norm, 0, 1)

with rasterio.open(OUT_NORM, "w", **meta) as dst:
    dst.write(norm.astype("float32"), 1)

print("✅ Distance to roads raster created")
print("➡", OUT_RASTER)
print("➡", OUT_NORM)
