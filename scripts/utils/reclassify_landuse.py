import rasterio
import numpy as np
from pathlib import Path

# =====================
# PATHS
# =====================
IN_LULC = Path("data/processed/lulc_worldcover_aoi.tif")
OUT = Path("data/processed/lulc_suitability.tif")
OUT.parent.mkdir(parents=True, exist_ok=True)

NODATA = -9999

# =====================
# RECLASS TABLE
# =====================
RECLASS = {
    10: 0.3,   # Tree cover
    20: 0.6,   # Shrubland
    30: 0.8,   # Grassland
    40: 1.0,   # Cropland
    50: 0.0,   # Built-up
    60: 0.5,   # Bare
    70: 0.0,   # Snow / ice
    80: 0.0,   # Water
    90: 0.2,   # Wetland
    95: 0.0,   # Mangroves
    100: 0.0   # Moss / lichen
}

# =====================
# PROCESS
# =====================
def reclassify():
    with rasterio.open(IN_LULC) as src:
        data = src.read(1)
        meta = src.meta.copy()

    out = np.full(data.shape, NODATA, dtype="float32")

    for code, value in RECLASS.items():
        out[data == code] = value

    meta.update(
        dtype="float32",
        nodata=NODATA,
        compress="lzw"
    )

    with rasterio.open(OUT, "w", **meta) as dst:
        dst.write(out, 1)

    print("✔ Land use suitability raster created:")
    print(OUT)


if __name__ == "__main__":
    reclassify()
