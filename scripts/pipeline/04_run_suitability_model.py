import rasterio
import numpy as np
from pathlib import Path

# =========================
# Inputs
# =========================
RASters = {
    "landuse": ("data/processed/lulc_suitability.tif", 0.30),
    "roads": ("data/processed/roads_distance_norm.tif", 0.25),
    "slope": ("data/processed/slope_norm.tif", 0.20),
    "elevation": ("data/processed/elevation_norm.tif", 0.15),
}

OUT = Path("data/processed/suitability.tif")
OUT.parent.mkdir(parents=True, exist_ok=True)

def run_model():
    arrays = []
    weights = []

    profile = None

    for name, (path, weight) in RASters.items():
        with rasterio.open(path) as src:
            arr = src.read(1).astype("float32")
            arrays.append(arr)
            weights.append(weight)
            if profile is None:
                profile = src.profile

    suitability = np.zeros_like(arrays[0], dtype="float32")

    for arr, w in zip(arrays, weights):
        suitability += arr * w

    profile.update(
        dtype="float32",
        nodata=0.0,
        compress="lzw"
    )

    with rasterio.open(OUT, "w", **profile) as dst:
        dst.write(suitability, 1)

    print("✅ Suitability model creado")
    print("➡", OUT)

if __name__ == "__main__":
    run_model()
