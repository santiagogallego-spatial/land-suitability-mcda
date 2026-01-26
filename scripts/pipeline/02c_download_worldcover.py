import requests
from pathlib import Path
import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np

# =====================
# PATHS
# =====================
BASE_GRID = Path("data/processed/base_grid.tif")
RAW_DIR = Path("data/external/worldcover")
OUT = Path("data/processed/lulc_worldcover_aoi.tif")

RAW_DIR.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)

# =====================
# WORLD COVER CONFIG
# =====================
VERSION = "v200"   # usar la más reciente
TILE = "N03W075"   # correcto para Cundinamarca

URL = (
    f"https://esa-worldcover.s3.eu-central-1.amazonaws.com/"
    f"{VERSION}/2021/map/"
    f"ESA_WorldCover_10m_2021_{VERSION}_{TILE}_Map.tif"
)

RAW_TILE = RAW_DIR / f"{TILE}_{VERSION}.tif"
NODATA = 0


# =====================
# DOWNLOAD
# =====================
def download_tile():
    if RAW_TILE.exists():
        print("✔ WorldCover tile already downloaded")
        return RAW_TILE

    print(f"⬇ Downloading WorldCover tile {TILE}...")
    print("URL:", URL)

    r = requests.get(URL, stream=True)
    r.raise_for_status()

    with open(RAW_TILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print("✔ Download complete:", RAW_TILE)
    return RAW_TILE


# =====================
# ALIGN TO BASE GRID
# =====================
def align_to_base(tile_path):
    print("✂ Aligning WorldCover to base_grid")

    with rasterio.open(BASE_GRID) as base:
        meta = base.meta.copy()
        dst_crs = base.crs
        dst_transform = base.transform
        height, width = base.height, base.width

    with rasterio.open(tile_path) as src:
        dst = np.full((height, width), NODATA, dtype="uint8")

        reproject(
            source=src.read(1),
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest,
        )

    meta.update(
        dtype="uint8",
        nodata=NODATA,
        compress="lzw",
        count=1
    )

    with rasterio.open(OUT, "w", **meta) as dstfile:
        dstfile.write(dst, 1)

    print("✔ LULC AOI created:", OUT)


# =====================
# MAIN
# =====================
if __name__ == "__main__":
    tile = download_tile()
    align_to_base(tile)
