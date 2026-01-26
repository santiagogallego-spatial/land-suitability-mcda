import geopandas as gpd

shp_path = r"C:\Users\galle\OneDrive - Universidad Nacional de Colombia\Universidad Nacional\UN 2024-2\Geomatica\Nestor\Colombia.shp"

gdf = gpd.read_file(shp_path)


municipio = gdf[gdf["MPIO_CDPMP"] == "25402"]

print(municipio.empty)
print(len(municipio))


municipio.to_file(
    r"data/raw/La_Vega.gpkg",
    driver="GPKG"
)

municipio = municipio.to_crs(epsg=9377)

minx, miny, maxx, maxy = municipio.total_bounds
print(minx, miny, maxx, maxy)
