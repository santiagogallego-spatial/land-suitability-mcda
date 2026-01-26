import rasterio
from rasterio.enums import Resampling  # <--- Acceso correcto para v1.3.9
import numpy as np
from esda.moran import Moran
from libpysal.weights import lat2W
from pathlib import Path

# 1. PATH CONFIGURATION
BASE_DIR = Path("C:/Users/galle/OneDrive/Documentos/Freelance_2026/0_Portafolio/Land_suitability")
RASTER_PATH = BASE_DIR / "data/processed/suitability_final.tif"

try:
    with rasterio.open(RASTER_PATH) as src:
        # Downsample for computational efficiency (1/10 of original size)
        new_height = src.height // 10
        new_width = src.width // 10
        
        # Correct Resampling call for Rasterio 1.3.9
        data = src.read(
            1, 
            out_shape=(new_height, new_width), 
            resampling=Resampling.bilinear
        )
        
        # Clean data: Replace NaNs and NoData with 0
        data = np.where(np.isnan(data) | (data < 0), 0, data)

        print(f"📊 Analysis Matrix: {data.shape[0]}x{data.shape[1]} pixels")

        # 2. SPATIAL WEIGHTS MATRIX (ROOK)
        # We define neighbors in a grid
        w = lat2W(data.shape[0], data.shape[1])
        w.transform = 'R' # Row-standardization

        # 3. CALCULATE MORAN'S I
        # .flatten() is required to pass the 2D grid as a 1D vector
        mi = Moran(data.flatten(), w)

        print(f"\n--- SPATIAL AUTOCORRELATION REPORT ---")
        print(f"Moran's I Statistic: {mi.I:.4f}")
        print(f"Expectation: {mi.EI:.4f}")
        print(f"P-value: {mi.p_sim:.4f}")
        print(f"Z-score: {mi.z_sim:.4f}")

        # 4. PROFESSIONAL INTERPRETATION
        print("\nConclusion (English):")
        if mi.p_sim < 0.05:
            if mi.I > mi.EI:
                print("✅ CLUSTERED: High suitability areas are geographically concentrated.")
            else:
                print("⚠️ DISPERSED: Suitability follows a competitive/checkerboard pattern.")
        else:
            print("🎲 RANDOM: No significant spatial pattern detected.")

except Exception as e:
    print(f"❌ Error during spatial analysis: {e}")