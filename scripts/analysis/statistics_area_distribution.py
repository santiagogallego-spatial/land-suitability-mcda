import rasterio
import numpy as np
import pandas as pd
from pathlib import Path

# 1. Configuración de rutas
BASE_DIR = Path("C:/Users/galle/OneDrive/Documentos/Freelance_2026/0_Portafolio/Land_suitability")
RASTER_PATH = BASE_DIR / "data/processed/suitability_final.tif"

def generate_suitability_stats(raster_path):
    with rasterio.open(raster_path) as src:
        # Leer la banda 1
        data = src.read(1)
        # Obtener resolución (suponiendo píxeles cuadrados en metros)
        pixel_size_x, pixel_size_y = src.res
        pixel_area_m2 = abs(pixel_size_x * pixel_size_y)
        
        # Máscara para ignorar valores NoData (suelen ser 0 o -9999)
        # Ajusta el umbral si tu raster tiene valores válidos en 0
        valid_data = data[data > -0.01] 
        
        # 2. Definir rangos de clasificación
        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
        
        # Clasificar los píxeles
        counts, _ = np.histogram(valid_data, bins=bins)
        
        # 3. Cálculos de área
        areas_ha = (counts * pixel_area_m2) / 10000
        percentages = (counts / len(valid_data)) * 100
        
        # 4. Crear DataFrame resumen
        df = pd.DataFrame({
            'Suitability Level': labels,
            'Pixel Count': counts,
            'Area (Ha)': np.round(areas_ha, 2),
            'Percentage (%)': np.round(percentages, 2)
        })
        
        return df

# Ejecutar y mostrar resultados
try:
    stats_df = generate_suitability_stats(RASTER_PATH)
    print("\n--- RESUMEN ESTADÍSTICO DE APTITUD ---")
    print(stats_df.to_string(index=False))
    
    # Guardar a CSV para adjuntar al informe
    output_csv = BASE_DIR / "outputs/suitability_statistics.csv"
    stats_df.to_csv(output_csv, index=False)
    print(f"\n✅ Estadísticas guardadas en: {output_csv}")

except Exception as e:
    print(f"❌ Error al procesar: {e}")