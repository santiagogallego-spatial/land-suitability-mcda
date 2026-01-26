import os
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
)

# --- Configuración del proyecto ---
PROJECT_FOLDER = "qgis/projects"
PROJECT_NAME = "suitability.qgs"

TARGET_CRS = "EPSG:9377"  # MAGNA SIRGAS

# Rutas absolutas a tus rasters
BASE_GRID_PATH = os.path.abspath("data/processed/base_grid.tif")
DEM_PATH = os.path.abspath("data/raw/dem_lavega.tif")

# --- Inicializar QGIS (Standalone) ---
qgs = QgsApplication([], False)
qgs.initQgis()

# --- Crear proyecto ---
project = QgsProject.instance()
project.setCrs(QgsRasterLayer(BASE_GRID_PATH).crs())  # opcional, se puede forzar TARGET_CRS después

# --- Agregar capas ---
layers = []

if os.path.exists(BASE_GRID_PATH):
    base_grid_layer = QgsRasterLayer(BASE_GRID_PATH, "Base Grid")
    if base_grid_layer.isValid():
        layers.append(base_grid_layer)
    else:
        print(f"Error: Base Grid inválido: {BASE_GRID_PATH}")
else:
    print(f"No se encontró Base Grid: {BASE_GRID_PATH}")

if os.path.exists(DEM_PATH):
    dem_layer = QgsRasterLayer(DEM_PATH, "DEM La Vega")
    if dem_layer.isValid():
        layers.append(dem_layer)
    else:
        print(f"Error: DEM inválido: {DEM_PATH}")
else:
    print(f"No se encontró DEM: {DEM_PATH}")

# Agregar las capas al proyecto
for layer in layers:
    project.addMapLayer(layer)

# --- Guardar proyecto ---
os.makedirs(PROJECT_FOLDER, exist_ok=True)
project_path = os.path.join(PROJECT_FOLDER, PROJECT_NAME)
project.write(project_path)

print(f"Proyecto QGIS creado en: {project_path}")

# --- Finalizar QGIS ---
qgs.exitQgis()