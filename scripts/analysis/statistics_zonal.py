import pandas as pd
import matplotlib
# Force a non-interactive backend to avoid window conflicts in VS Code
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from pathlib import Path

# Path configuration
BASE_DIR = Path("C:/Users/galle/OneDrive/Documentos/Freelance_2026/0_Portafolio/Land_suitability")
CSV_PATH = BASE_DIR / "outputs/suitability_statistics.csv"
OUTPUT_IMG = BASE_DIR / "outputs/suitability_chart.png"

try:
    # Load data
    df = pd.read_csv(CSV_PATH)

    # Professional traffic-light colors
    colors = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['Suitability Level'], df['Area (Ha)'], color=colors, edgecolor='black', alpha=0.8)

    # Add data labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.01), 
                 f'{yval:,.1f} Ha', ha='center', va='bottom', fontweight='bold')

    # Chart formatting in English
    plt.title('Area Distribution by Suitability Level', fontsize=14, fontweight='bold')
    plt.xlabel('Suitability Level', fontsize=12)
    plt.ylabel('Area (Hectares)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Final adjustments and export
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300)
    print(f"✅ Chart exported successfully to: {OUTPUT_IMG}")

except Exception as e:
    print(f"❌ Error generating the chart: {e}")