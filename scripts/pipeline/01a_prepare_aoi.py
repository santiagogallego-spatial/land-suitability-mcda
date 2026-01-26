from pyproj import Transformer
from config.aoi import BBOX_WGS84, AOI_CRS, TARGET_CRS, AOI_NAME

transformer = Transformer.from_crs(
    AOI_CRS,
    TARGET_CRS,
    always_xy=True
)

xmin, ymin = transformer.transform(
    BBOX_WGS84["lon_min"],
    BBOX_WGS84["lat_min"]
)

xmax, ymax = transformer.transform(
    BBOX_WGS84["lon_max"],
    BBOX_WGS84["lat_max"]
)

print("AOI:", AOI_NAME)
print("CRS destino:", TARGET_CRS)
print("Bounding box proyectado (m):")
print(f"xmin: {xmin:.2f}")
print(f"ymin: {ymin:.2f}")
print(f"xmax: {xmax:.2f}")
print(f"ymax: {ymax:.2f}")
