import rasterio

with rasterio.open("data/processed/base_grid.tif") as src:
    print(src.crs)
    print(src.count)
    print(src.width, src.height)