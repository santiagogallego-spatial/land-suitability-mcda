import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np
import os

BASE_GRID = "data/processed/base_grid.tif"
DEM_RAW = "data/raw/dem_lavega.tif"

OUT_ELEV_RAW = "data/processed/elevation_raw.tif"
OUT_ELEV_NORM = "data/processed/elevation_norm.tif"

NODATA = -9999


def process_elevation():
    with rasterio.open(BASE_GRID) as base:
        base_meta = base.meta.copy()
        base_shape = (base.height, base.width)
        base_transform = base.transform
        base_crs = base.crs

    with rasterio.open(DEM_RAW) as dem:
        dem_data = dem.read(1)
        dem_transform = dem.transform
        dem_crs = dem.crs

        elevation = np.full(base_shape, NODATA, dtype="float32")

        reproject(
            source=dem_data,
            destination=elevation,
            src_transform=dem_transform,
            src_crs=dem_crs,
            dst_transform=base_transform,
            dst_crs=base_crs,
            resampling=Resampling.bilinear,
            dst_nodata=NODATA
        )

    # =========================
    # Guardar elevación cruda
    # =========================
    meta = base_meta
    meta.update({
        "dtype": "float32",
        "nodata": NODATA,
        "compress": "lzw"
    })

    os.makedirs("data/processed", exist_ok=True)

    with rasterio.open(OUT_ELEV_RAW, "w", **meta) as dst:
        dst.write(elevation, 1)

    print("✔ Elevación reproyectada y alineada")

    # =========================
    # Normalización 0–1
    # =========================
    mask = elevation != NODATA
    elev_min = elevation[mask].min()
    elev_max = elevation[mask].max()

    elevation_norm = np.full_like(elevation, NODATA, dtype="float32")
    elevation_norm[mask] = (elevation[mask] - elev_min) / (elev_max - elev_min)

    with rasterio.open(OUT_ELEV_NORM, "w", **meta) as dst:
        dst.write(elevation_norm, 1)

    print("✔ Elevación normalizada (0–1)")
    print(f"Rango elevación: {elev_min:.1f} – {elev_max:.1f} m")


if __name__ == "__main__":
    process_elevation()
