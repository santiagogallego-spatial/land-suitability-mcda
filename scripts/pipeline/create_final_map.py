import sys
import os
from pathlib import Path
from qgis.core import (
    QgsApplication, QgsProject, QgsRasterLayer, QgsPrintLayout,
    QgsLayoutItemMap, QgsLayoutItemLabel, QgsLayoutItemLegend,
    QgsLayoutItemScaleBar, QgsLayoutItemPicture,
    QgsLayoutExporter, QgsUnitTypes, QgsLayoutPoint, QgsLayoutSize,
    QgsLayoutItemPage, QgsRectangle, QgsLegendStyle, QgsTextFormat
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# 1. INICIALIZAR QGIS
QGIS_INSTALL_PATH = r"C:\Program Files\QGIS 3.44.6\apps\qgis"
QgsApplication.setPrefixPath(QGIS_INSTALL_PATH, True)
qgs = QgsApplication([], True)
qgs.initQgis()

project = QgsProject.instance()
project.clear()

# 2. RUTAS
BASE_DIR = Path("C:/Users/galle/OneDrive/Documentos/Freelance_2026/0_Portafolio/Land_suitability")
RASTER_FINAL = BASE_DIR / "data/processed/suitability_final.tif"
RASTER_BASE_LOCAL = BASE_DIR / "data/raw/mapa_base.tif" 
OUTPUT_PDF = BASE_DIR / "outputs/mapa_entregable_final_km_v13.pdf"

# 3. CARGAR CAPAS
base_layer = QgsRasterLayer(str(RASTER_BASE_LOCAL), "Base Map")
raster = QgsRasterLayer(str(RASTER_FINAL), "Suitability")

if RASTER_FINAL.with_suffix('.qml').exists():
    raster.loadNamedStyle(str(RASTER_FINAL.with_suffix('.qml')))

raster.setOpacity(1.0)
project.addMapLayer(base_layer)
project.addMapLayer(raster)

# 4. CONFIGURAR LAYOUT
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.pageCollection().clear()
page = QgsLayoutItemPage(layout)
page.setPageSize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))
layout.pageCollection().addPage(page)

# --- MAPA ---
map_item = QgsLayoutItemMap(layout)
map_item.attemptResize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))
map_item.setLayers([raster, base_layer])
map_item.setBackgroundEnabled(False) 

# Encuadre exacto (con el offset de 2200 que te gustó)
raster_center = raster.extent().center()
target_center_y = raster_center.y() + 2200 
map_item.zoomToExtent(raster.extent())
map_item.setScale(map_item.scale() * 0.60) 
rect = map_item.extent()
final_extent = QgsRectangle(raster_center.x() - rect.width()/2, target_center_y - rect.height()/2,
                            raster_center.x() + rect.width()/2, target_center_y + rect.height()/2)
map_item.setExtent(final_extent)
layout.addLayoutItem(map_item)

# --- TÍTULO (8MM) ---
title = QgsLayoutItemLabel(layout)
title.setText("MULTI-CRITERIA LAND SUITABILITY MAP") 
t_fmt = QgsTextFormat()
t_fmt.setFont(QFont("Arial", 32, QFont.Bold))
t_fmt.setSize(8) 
t_fmt.setSizeUnit(QgsUnitTypes.RenderMillimeters) 
t_fmt.buffer().setEnabled(True)
t_fmt.buffer().setSize(2.0)
t_fmt.buffer().setColor(QColor("white"))
title.setTextFormat(t_fmt)
title.setHAlign(Qt.AlignCenter)
title.attemptResize(QgsLayoutSize(280, 40, QgsUnitTypes.LayoutMillimeters))
title.attemptMove(QgsLayoutPoint(8.5, 5, QgsUnitTypes.LayoutMillimeters)) 
layout.addLayoutItem(title)

# --- FLECHA DE NORTE ---
north_arrow = QgsLayoutItemPicture(layout)
svg_path = QGIS_INSTALL_PATH + "/svg/arrows/NorthArrow_04.svg"
north_arrow.setPicturePath(svg_path)
north_arrow.attemptResize(QgsLayoutSize(18, 18, QgsUnitTypes.LayoutMillimeters))
north_arrow.attemptMove(QgsLayoutPoint(12, 10, QgsUnitTypes.LayoutMillimeters)) 
layout.addLayoutItem(north_arrow)

# --- REGLA DE ESCALA (CORREGIDA PARA QGIS 3.44) ---
scale_bar = QgsLayoutItemScaleBar(layout)
scale_bar.setLinkedMap(map_item)
scale_bar.setUnits(QgsUnitTypes.DistanceKilometers)
scale_bar.setUnitLabel('km')

# LA CORRECCIÓN CLAVE:
# Cambiamos setMapUnitsPerLayoutUnit -> setMapUnitsPerScaleBarUnit
scale_bar.setMapUnitsPerScaleBarUnit(1000) 

scale_bar.setNumberOfSegments(4)
scale_bar.setUnitsPerSegment(2) 
scale_bar.setStyle('Double Box') 
scale_bar.setFont(QFont("Arial", 10, QFont.Bold))
scale_bar.applyDefaultSize()
scale_bar.attemptMove(QgsLayoutPoint(15, 185, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(scale_bar)

# --- LEYENDA (LIMPIEZA DE DECIMALES) ---
legend = QgsLayoutItemLegend(layout)
legend.setTitle("SUITABILITY SCORE")
legend.setLinkedMap(map_item)
legend.setSymbolWidth(20)
legend.setSymbolHeight(40)
legend.rstyle(QgsLegendStyle.Title).setFont(QFont("Arial", 12, QFont.Bold))
legend.rstyle(QgsLegendStyle.Title).setMargin(QgsLegendStyle.Bottom, 3)

legend.setAutoUpdateModel(False)
root = legend.model().rootGroup()
root.clear()
layer_node = root.addLayer(raster)
layer_node.setName("")

legend.refresh() 
nodes = legend.model().layerLegendNodes(layer_node)
if nodes:
    for i, node in enumerate(nodes):
        if i == 0:
            node.setUserLabel("1.0 (High)")
        elif i == len(nodes) - 1:
            node.setUserLabel("0.0 (Low)")
        else:
            node.setUserLabel("") 

legend.rstyle(QgsLegendStyle.SymbolLabel).setFont(QFont("Arial", 10, QFont.Bold))
legend.setBackgroundEnabled(False)
legend.attemptResize(QgsLayoutSize(60, 100, QgsUnitTypes.LayoutMillimeters))
legend.attemptMove(QgsLayoutPoint(245, 105, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(legend)

# 5. EXPORTACIÓN
exporter = QgsLayoutExporter(layout)
settings = QgsLayoutExporter.PdfExportSettings()
settings.rasterizeWholeLayout = True 

result = exporter.exportToPdf(str(OUTPUT_PDF), settings)
if result == QgsLayoutExporter.Success:
    print(f"✅ ¡Misión cumplida! Mapa final en KM generado: {OUTPUT_PDF}")

qgs.exitQgis()