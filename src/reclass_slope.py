from pathlib import Path
import rasterio
import numpy as np
import os

BASE_DIR = Path(__file__).resolve().parents[1]

SLOPE_PATH = BASE_DIR / "data" / "processed" / "slope_lavega.tif"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "slope_suitability.tif"

def reclassify_slope():
    with rasterio.open(SLOPE_PATH) as src:
        slope = src.read(1)
        meta = src.meta.copy()

    # Create empty suitability raster
    suitability = np.zeros_like(slope, dtype=np.uint8)

    suitability[(slope >= 0) & (slope < 5)] = 5
    suitability[(slope >= 5) & (slope < 10)] = 4
    suitability[(slope >= 10) & (slope < 20)] = 3
    suitability[(slope >= 20) & (slope < 30)] = 2
    suitability[slope >= 30] = 1

    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)

    meta.update(dtype=rasterio.uint8, nodata=0)

    with rasterio.open(OUTPUT_PATH, "w", **meta) as dst:
        dst.write(suitability, 1)

    print("Slope suitability raster created:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    reclassify_slope()
