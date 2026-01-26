import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Configuración de capas y pesos
RASters = {
    "landuse": ("data/processed/lulc_suitability.tif", 0.30),
    "roads": ("data/processed/roads_distance_norm.tif", 0.25),
    "slope": ("data/processed/slope_norm.tif", 0.20),
    "elevation": ("data/processed/elevation_norm.tif", 0.15),
}

def load_raster_flat(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype('float32')
        data[data == src.nodata] = np.nan
        return data.flatten()

print("Cargando datos y calculando sensibilidad...")
data_dict = {}
aptitud_temp = None

for nombre, (ruta, peso) in RASters.items():
    valores = load_raster_flat(ruta)
    data_dict[nombre] = valores
    if aptitud_temp is None:
        aptitud_temp = valores * peso
    else:
        aptitud_temp += (valores * peso)

data_dict["aptitud_final"] = aptitud_temp
df = pd.DataFrame(data_dict).dropna()

# 2. Cálculo de Correlación
correlaciones = df.corr()['aptitud_final'].drop('aptitud_final').sort_values(ascending=False)

print("\n--- Resultados de Sensibilidad ---")
print(correlaciones)

# 3. Visualización integrada
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

# Crear el gráfico de barras
ax = sns.barplot(x=correlaciones.values, y=correlaciones.index, hue=correlaciones.index, palette="viridis", legend=False)

# Personalización
plt.title("Sensitivity of Variables (Correlation with Final Aptitude)", fontsize=14, pad=20)
plt.xlabel("Pearson's correlation coefficient", fontsize=12)
plt.ylabel("Input Layers", fontsize=12)
plt.xlim(0, 1) # The correlation is usually positive here.

# Add value labels to the bars
for i, v in enumerate(correlaciones.values):
    ax.text(v + 0.02, i, f"{v:.2f}", color='black', va='center', fontweight='bold')

# Guardar y mostrar
output_path = "outputs/correlation_plot.png"
os.makedirs("results", exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
print(f"\nGráfico guardado exitosamente en: {output_path}")
plt.show()