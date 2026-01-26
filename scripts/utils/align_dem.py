# scripts/align_dem.py

import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_GRID = Path("data/processed/base_grid.tif")
DEM_RAW = Path("data/raw/dem_lavega.tif")
DEM_OUT = Path("data/processed/dem_aligned.tif")

DEM_OUT.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Read base grid (reference)
# -----------------------------
with rasterio.open(BASE_GRID) as base:
    dst_crs = base.crs
    dst_transform = base.transform
    dst_width = base.width
    dst_height = base.height
    dst_nodata = base.nodata

# -----------------------------
# Read DEM source
# -----------------------------
with rasterio.open(DEM_RAW) as src:
    src_array = src.read(1)
    src_transform = src.transform
    src_crs = src.crs
    src_nodata = src.nodata

    # Destination array
    dst_array = np.full(
        (dst_height, dst_width),
        dst_nodata,
        dtype=np.float32
    )

    # -----------------------------
    # Reproject + resample
    # -----------------------------
    reproject(
        source=src_array,
        destination=dst_array,
        src_transform=src_transform,
        src_crs=src_crs,
        src_nodata=src_nodata,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        dst_nodata=dst_nodata,
        resampling=Resampling.bilinear
    )

# -----------------------------
# Save aligned DEM
# -----------------------------
with rasterio.open(
    DEM_OUT,
    "w",
    driver="GTiff",
    height=dst_height,
    width=dst_width,
    count=1,
    dtype=np.float32,
    crs=dst_crs,
    transform=dst_transform,
    nodata=dst_nodata,
    compress="lzw"
) as dst:
    dst.write(dst_array, 1)

print("DEM alineado correctamente")
print(f"Archivo: {DEM_OUT}")
