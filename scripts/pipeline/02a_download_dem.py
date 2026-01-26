"""
Script: download_and_merge_dem.py
Función: Descargar todos los tiles SRTM necesarios para un AOI
         y combinarlos en un solo archivo DEM.
"""

import os
import numpy as np
import rasterio
from rasterio.merge import merge
import requests
import gzip
import shutil

# ==========================
# Configuración AOI
# ==========================
AOI_NAME = "La Vega, Cundinamarca"
BBOX_WGS84 = {
    "lon_min": -74.38,
    "lat_min": 4.95,
    "lon_max": -74.28,
    "lat_max": 5.05
}

OUTPUT_DIR = "data/raw"
MERGED_DEM_PATH = os.path.join(OUTPUT_DIR, "dem_lavega.tif")

SRTM_BASE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/skadi"

# ==========================
# Funciones
# ==========================

def deg_to_tile(lat, lon):
    """Convierte lat/lon a nombre de tile SRTM (1° x 1°), esquina SW."""
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    lat_deg = int(np.floor(lat))
    lon_deg = int(np.floor(lon))
    return f"{ns}{lat_deg:02d}{ew}{abs(lon_deg):03d}.hgt.gz"

def download_tile(tile_name):
    """Descarga un tile SRTM si no existe localmente."""
    lat_prefix = tile_name[0:3]  # Ej: N04
    output_path = os.path.join(OUTPUT_DIR, tile_name)
    if os.path.exists(output_path.replace(".gz", "")):
        print(f"Tile ya existe: {tile_name}")
        return output_path.replace(".gz", "")
    
    url = f"{SRTM_BASE_URL}/{lat_prefix}/{tile_name}"
    print("Descargando", tile_name)
    print("URL:", url)
    
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise ValueError(f"No se pudo descargar {tile_name}. Status code: {response.status_code}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Guardar el .gz
    gz_path = output_path
    with open(gz_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    # Descomprimir
    dem_path = gz_path.replace(".gz", "")
    with gzip.open(gz_path, "rb") as f_in, open(dem_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    print("Tile descargado y descomprimido:", dem_path)
    return dem_path

def download_dem_for_aoi(bbox):
    """Descarga todos los tiles necesarios y devuelve lista de paths."""
    lat_min, lat_max = bbox["lat_min"], bbox["lat_max"]
    lon_min, lon_max = bbox["lon_min"], bbox["lon_max"]
    
    # Determinar rango de tiles
    latitudes = range(int(np.floor(lat_min)), int(np.ceil(lat_max)))
    longitudes = range(int(np.floor(lon_min)), int(np.ceil(lon_max)))
    
    tile_paths = []
    for lat in latitudes:
        for lon in longitudes:
            tile_name = deg_to_tile(lat, lon)
            try:
                dem_path = download_tile(tile_name)
                tile_paths.append(dem_path)
            except ValueError as e:
                print(e)
    
    if not tile_paths:
        raise RuntimeError("No se descargó ningún tile para el AOI.")
    
    return tile_paths

def merge_tiles(tile_paths, output_path):
    """Combina varios DEM en uno solo."""
    src_files = [rasterio.open(p) for p in tile_paths]
    mosaic, out_trans = merge(src_files)
    
    out_meta = src_files[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "compress": "lzw"
    })
    
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(mosaic)
    
    for src in src_files:
        src.close()
    
    print(f"DEM combinado creado: {output_path}")
    return output_path

# ==========================
# Main
# ==========================
if __name__ == "__main__":
    tiles = download_dem_for_aoi(BBOX_WGS84)
    merge_tiles(tiles, MERGED_DEM_PATH)
