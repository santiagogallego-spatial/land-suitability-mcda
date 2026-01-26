import rasterio
from rasterio.transform import from_origin
import numpy as np

from config.aoi import (
    AOI_NAME,
    TARGET_CRS,
    BBOX_PROJECTED
)

# =========================
# Base raster parameters
# =========================
RESOLUTION = 30  # meters
INITIAL_VALUE = 1  # valor seguro para evitar errores en QGIS
NODATA = -9999    # aún se mantiene para referencia si lo necesitas después

def create_base_grid():
    xmin, ymin, xmax, ymax = BBOX_PROJECTED

    width = int((xmax - xmin) / RESOLUTION)
    height = int((ymax - ymin) / RESOLUTION)

    transform = from_origin(
        xmin,
        ymax,  # origen arriba a la izquierda
        RESOLUTION,
        RESOLUTION
    )

    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": TARGET_CRS,
        "transform": transform,
        "nodata": NODATA,
        "compress": "lzw"
    }

    output_path = "data/processed/base_grid.tif"

    # Inicializar con valor seguro
    with rasterio.open(output_path, "w", **profile) as dst:
        data = np.full((height, width), INITIAL_VALUE, dtype="float32")
        dst.write(data, 1)

    print("Raster base creado:")
    print(f"AOI: {AOI_NAME}")
    print(f"Resolución: {RESOLUTION} m")
    print(f"Tamaño: {width} x {height}")
    print(f"Archivo: {output_path}")

if __name__ == "__main__":
    create_base_grid()
