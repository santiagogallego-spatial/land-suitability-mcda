import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.enums import Resampling as ResamplingEnum

# Paths
DEM_RAW = "data/raw/dem_lavega.tif"
BASE_GRID = "data/processed/base_grid.tif"
OUT_SLOPE = "data/processed/slope_norm.tif"

MAX_SLOPE = 40.0  # % (cap para normalización)


def compute_slope(dem, transform):
    """
    Calcula pendiente (%) usando diferencias centrales
    """
    xres = transform.a
    yres = -transform.e

    dzdx = np.gradient(dem, axis=1) / xres
    dzdy = np.gradient(dem, axis=0) / yres

    slope_rad = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
    slope_pct = np.tan(slope_rad) * 100

    return slope_pct


with rasterio.open(BASE_GRID) as ref:
    profile = ref.profile
    ref_data = ref.read(1)
    ref_transform = ref.transform
    ref_crs = ref.crs
    height, width = ref_data.shape

with rasterio.open(DEM_RAW) as src:
    dem_reproj = np.empty((height, width), dtype=np.float32)

    reproject(
        source=rasterio.band(src, 1),
        destination=dem_reproj,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=ref_transform,
        dst_crs=ref_crs,
        resampling=Resampling.bilinear
    )

# Calculate slope
slope = compute_slope(dem_reproj, ref_transform)

# Limit and normalise
slope = np.clip(slope, 0, MAX_SLOPE)
slope_norm = slope / MAX_SLOPE

# Save raster
profile.update(
    dtype="float32",
    nodata=-9999,
    count=1
)

with rasterio.open(OUT_SLOPE, "w", **profile) as dst:
    dst.write(slope_norm.astype(np.float32), 1)

print("Pendiente calculada y normalizada:")
print(f"Archivo: {OUT_SLOPE}")
print(f"Rango esperado: 0–1")
