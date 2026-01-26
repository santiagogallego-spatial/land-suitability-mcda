import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np
import os

BASE_GRID = "data/processed/base_grid.tif"
LANDUSE_VECTOR = "data/raw/landuse.shp"
OUT_LANDUSE = "data/processed/landuse_suitability.tif"

NODATA = -9999

# =========================
# Reclasificación experta
# =========================
LANDUSE_SCORES = {
    "forest": 0.1,
    "urban": 0.0,
    "agriculture": 0.8,
    "pasture": 0.7,
    "water": 0.0,
    "bare": 0.6
}


def process_landuse():
    # Base grid
    with rasterio.open(BASE_GRID) as base:
        meta = base.meta.copy()
        transform = base.transform
        shape = (base.height, base.width)
        crs = base.crs

    # Land use vector
    gdf = gpd.read_file(LANDUSE_VECTOR).to_crs(crs)

    # Convertir clases a valores numéricos
    gdf["suitability"] = gdf["class"].map(LANDUSE_SCORES)

    if gdf["suitability"].isna().any():
        missing = gdf[gdf["suitability"].isna()]["class"].unique()
        raise ValueError(f"Clases sin definir en LANDUSE_SCORES: {missing}")

    shapes = (
        (geom, value)
        for geom, value in zip(gdf.geometry, gdf["suitability"])
    )

    landuse_raster = rasterize(
        shapes=shapes,
        out_shape=shape,
        transform=transform,
        fill=NODATA,
        dtype="float32"
    )

    meta.update({
        "dtype": "float32",
        "nodata": NODATA,
        "compress": "lzw"
    })

    os.makedirs("data/processed", exist_ok=True)

    with rasterio.open(OUT_LANDUSE, "w", **meta) as dst:
        dst.write(landuse_raster, 1)

    print("✔ Land use procesado")
    print(f"Archivo: {OUT_LANDUSE}")
    print("Clases usadas:")
    for k, v in LANDUSE_SCORES.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    process_landuse()
