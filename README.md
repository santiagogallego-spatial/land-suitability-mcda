# Land Suitability Analysis using Multi-Criteria Decision Analysis (MCDA)

## Overview
This project implements a **land suitability analysis** based on **Multi-Criteria Decision Analysis (MCDA)** techniques using geospatial data.  
It is designed to support **agricultural planning and territorial decision-making** by integrating multiple spatial criteria into a single suitability index.

The workflow is fully **replicable and adaptable** to different regions, crops, or land-use scenarios.

---

## Objectives
- Integrate multiple spatial criteria affecting land suitability
- Normalize heterogeneous geospatial layers into a common scale
- Apply user-defined weights to each criterion
- Generate a final land suitability map using weighted overlay
- Classify suitability levels for decision support

---

## Methodology
The analysis follows a standardized MCDA workflow commonly used in professional GIS projects:

1. **Spatial preprocessing**
   - Reprojection to a common CRS
   - Resolution and extent alignment
   - Clipping to the study area
   - NoData handling

2. **Criteria normalization**
   - Min–max scaling or reclassification
   - Conversion to a standardized suitability scale

3. **Weight assignment**
   - User-defined weights based on expert knowledge or decision rules
   - Weight normalization (sum = 1)

4. **Weighted overlay**
   - Raster-based aggregation of all criteria

5. **Final classification**
   - Suitability classes (e.g. low, medium, high)

---

## Potential Applications
- Agricultural land-use planning
- Crop suitability assessment
- Environmental management
- Territorial planning and zoning
- Feasibility studies for rural development projects

---

## Tools and Technologies
- Python
- GeoPandas
- Rasterio
- NumPy
- Matplotlib

---

## Outputs
- Continuous land suitability raster
- Classified suitability map
- Spatial statistics per suitability class
- Exportable GeoTIFF outputs

---

## Project Structure
```text
Land_suitability/
│
├─ src/              # Source code
├─ data/             # Input datasets
│   ├─ raw/
│   └─ processed/
├─ outputs/          # Results and maps
│   ├─ maps/
│   └─ tables/
├─ README.md
├─ requirements.txt
└─ .gitignore
``` 

## Reproducibility 
This project is fully reproducible.  
All dependencies are managed through a virtual environment and documented in `requirements.txt`.

---

## Author
**Santiago Gallego**  
Geospatial Analyst | GIS & Spatial Data Science