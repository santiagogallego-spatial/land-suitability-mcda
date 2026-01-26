"""
Area of Interest (AOI)
La Vega, Cundinamarca - Colombia
"""

from pyproj import Transformer

# ======================
# Metadatos
# ======================
AOI_NAME = "La Vega, Cundinamarca"

# ======================
# Sistemas de referencia
# ======================
AOI_CRS = "EPSG:4326"     # WGS84
TARGET_CRS = "EPSG:9377"  # MAGNA-SIRGAS / Colombia Bogota

# ======================
# Bounding box original
# ======================
BBOX_WGS84 = {
    "lon_min": -74.38,
    "lat_min": 4.95,
    "lon_max": -74.28,
    "lat_max": 5.05
}

# ======================
# Proyección del bbox
# ======================
_transformer = Transformer.from_crs(
    AOI_CRS,
    TARGET_CRS,
    always_xy=True
)

xmin, ymin = _transformer.transform(
    BBOX_WGS84["lon_min"],
    BBOX_WGS84["lat_min"]
)

xmax, ymax = _transformer.transform(
    BBOX_WGS84["lon_max"],
    BBOX_WGS84["lat_max"]
)

BBOX_PROJECTED = (xmin, ymin, xmax, ymax)
