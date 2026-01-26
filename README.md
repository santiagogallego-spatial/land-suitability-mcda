# 🌍 Land Suitability Intelligence: Municipal-Scale MCDA
### **Advanced Geospatial Decision Support System for AgTech & Territorial Planning**

---

## 🚀 Strategic Value Proposition
Identifying the optimal location for high-scale projects is a multi-million dollar challenge. This engine transforms fragmented environmental, physical, and logistical variables into a single **Suitability Score**, reducing the margin of error in land acquisition and zoning.

**Key Business Benefits:**
* **De-Risking Investments:** Identify legal or environmental "No-Go" zones before committing resources.
* **Operational Efficiency:** Pinpoint land clusters with the best slope and road proximity to minimize long-term CAPEX/OPEX.
* **Scientific Transparency:** Every pixel is backed by a mathematical weighting process, making the results auditable for stakeholders or regulators.

---

## 📊 Analytical Deliverables & Insights

### 1. Multi-Criteria Suitability Map
A high-resolution GeoTIFF (up to 10m/pixel) classifying the territory into 5 actionable levels: *Very Low, Low, Moderate, High, and Very High*.

### 2. Area Distribution Analytics
We don't just provide a map; we provide numbers. This includes a quantified breakdown of hectares available per suitability class to help calculate project feasibility.
> **Key Insight:** In our baseline model, we successfully filtered 18,348 Ha of "Very Low" suitability, focusing efforts on the top 10% of the territory.

### 3. Spatial Reliability Report (Statistical Validation)
To ensure the model isn't random, we run advanced spatial tests:
* **Global Moran's I:** Confirms that high-suitability areas are geographically clustered (essential for logistics).
* **Z-Score & P-Value:** Provides a 99% confidence level that the patterns found are statistically significant.
* **Pearson Correlation Matrix:** Ensures that input criteria are independent, avoiding "double-counting" bias in the final score.

---

## 🛠️ Technical Workflow & Criteria
The system uses a **Weighted Linear Combination (WLC)** method, the industry standard for MCDA in GIS.

| Criterion | Type | Rationale |
| :--- | :--- | :--- |
| **Slope (DEM)** | Restriction | Limits mechanization and increases erosion risk if >15%. |
| **LULC (WorldCover)** | Friction | Categorizes current land use (Forest, Grassland, Cropland). |
| **Logistics (Roads)** | Driver | Minimizes transport costs and improves market access. |
| **Elevation** | Driver |Constraint	Influences climate conditions, agricultural viability, and infrastructure costs. |
| **Protected Areas** | Exclusion | Masking out zones with legal/environmental restrictions. |

---

## 💻 Software Architecture
This is a **productized pipeline** built for reproducibility. It can be re-run with new weights in seconds to test different "What-if" scenarios.

```text
Land_suitability/
│
├─ scripts/                  # Source code
│    ├─ pipeline/
│    │     ├─ 01a_prepare_aoi.py
│    │     ├─ 01b_create_base_grid.py
│    │     ├─ 02a_download_dem.py
│    │     ├─ 02b_download_roads.py
│    │     ├─ 02c_download_worldcover.py
│    │     ├─ 03a_process_elevation.py
│    │     ├─ 03b_process_roads_distance.py
│    │     ├─ 03c_process_landuse.py
│    │     ├─ 03d_process_slope.py
│    │     ├─ 04_run_suitability_model
│    │     ├─ 05_create_final_map.py
│    │     └─ 05_create_final_report.py
│    │
│    ├─ analysis/
│    │     ├─ 01_area_distribution.py
│    │     ├─ 02_zonal_statistics.py
│    │     ├─ 03_Moran_test.py
│    │     └─ 04_Pearson_correlation.py
│    │
│    └─ utils/
│          ├─ align_dem.py
│          ├─ municipality.py
│          └─ reclassify_landuse.py
│
├─ data/                 # datasets
│   ├─ raw/
│   └─ processed/
│       ├─ lulc_suitability.tif
│       ├─ roads_distance_norm.tif
│       ├─ slope_norm.tif
│       └─ elevation_norm.tif
│
├─ outputs/              # Results   
│   ├─ maps/
│   │    └─ Final_map.pdf
│   │
│   ├─ plots_and_tables/
│   │    ├─ Area_distribution.csv
│   │    ├─ Area_distribution.png
│   │    └─ Correlation_plot.png
│   │
│   └─ report/
│        └─ final_report.pdf
│
├─ config/               # Configuration files (weights, rules)
├─ README.md
├─ requirements.txt  
└─ .gitignore 
```
---

## Reproducibility and Adaptability
This project is fully reproducible.  
All dependencies are managed through a virtual environment and documented in `requirements.txt`.

---

## Tools and Technologies
- Python
- PyQGIS (QGIS Processing Framework)
- Matplotlib
- numpy==1.26.4
- pandas==2.1.4
- pyproj==3.6.1
- rasterio==1.3.9
- fiona==1.9.5
- shapely==2.0.3
- geopandas==0.14.3
- scipy==1.11.4
 
---

## 👨‍💻 Author & Consultancy
**Santiago Gallego** Agronomist Engineer | Geospatial Software Developer I bridge the gap between **Agronomy**, **Data Science**, and **GIS** to provide actionable intelligence for the AgTech sector.

---

**Ready to optimize your land selection process?** 
