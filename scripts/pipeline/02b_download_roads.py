import osmnx as ox
import geopandas as gpd
from shapely.geometry import box
from pathlib import Path

from config.aoi import BBOX_WGS84, TARGET_CRS

OUT = Path("data/processed/roads.gpkg")
OUT.parent.mkdir(parents=True, exist_ok=True)

def download_roads():
    print("⬇ Downloading main roads from OpenStreetMap...")

    north = BBOX_WGS84["lat_max"]
    south = BBOX_WGS84["lat_min"]
    east = BBOX_WGS84["lon_max"]
    west = BBOX_WGS84["lon_min"]

    polygon = box(west, south, east, north)

    # 🚦 Vías relevantes para suitability
    tags = {
    "highway": [
        "primary",
        "secondary",
        "tertiary",
        "trunk",
    ]
    }


    

    gdf = ox.features_from_polygon(
        polygon,
        tags=tags
    )

    # Solo geometrías lineales
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]

    # Reproyectar
    gdf = gdf.to_crs(TARGET_CRS)

    gdf.to_file(OUT, driver="GPKG")

    print(f"✔ Roads saved to {OUT}")

if __name__ == "__main__":
    download_roads()
