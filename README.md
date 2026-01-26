# Land Suitability Analysis  
### Municipal-Scale Multi-Criteria Decision Analysis (MCDA)

## Overview
This project implements a **municipal-scale land suitability analysis** using **Multi-Criteria Decision Analysis (MCDA)** and geospatial data.  
It is designed to support **agricultural and territorial planning**, integrating physical, environmental, and accessibility-related criteria into a single, interpretable suitability index.

The workflow is **fully reproducible, configurable, and adaptable** to different municipalities, regions, or land-use scenarios using publicly available data.

---

## Study Area
The methodology is intended for **municipal-level applications** (approximately 10,000–300,000 hectares), where decision-makers require spatially explicit evidence to guide land-use planning, agricultural development, or zoning processes.

The analysis can be applied to any municipality provided that basic geospatial datasets are available.

---

## Objectives
- Identify areas with higher land suitability based on multiple spatial criteria
- Integrate heterogeneous geospatial datasets into a unified analytical framework
- Normalize and weight criteria according to planning priorities
- Produce clear and interpretable suitability maps for decision support
- Ensure transparency and reproducibility of the analysis

---

## Suitability Criteria
The baseline implementation uses a compact and defensible set of criteria commonly applied in professional GIS-based suitability studies:

| Criterion | Description | Role |
|---------|------------|------|
| Slope | Terrain steepness derived from a Digital Elevation Model (DEM) | Limiting |
| Land Use / Land Cover (LULC) | Current land use classification | Restrictive |
| Distance to Roads | Accessibility and transportation efficiency | Positive |
| Distance to Settlements | Proximity to population centers and services | Positive |
| Environmental Constraints | Protected or restricted areas | Exclusion |

All criteria can be modified, added, or removed depending on the planning objective.

---

## Methodology
The analysis follows a standardized MCDA workflow commonly used in applied GIS projects:

### 1. Spatial Preprocessing
- Reprojection to a common Coordinate Reference System (CRS)
- Raster alignment (resolution and extent)
- Clipping to the municipal boundary
- NoData and mask handling

### 2. Criteria Standardization
- Normalization of continuous variables (e.g. slope, distances)
- Reclassification of categorical layers (e.g. land use)
- Conversion to a common suitability scale

### 3. Weight Assignment
- User-defined weights based on expert judgment or planning priorities
- Weight normalization to ensure consistency

### 4. Weighted Overlay
- Raster-based aggregation of all standardized criteria into a continuous suitability index

### 5. Final Classification
- Classification of suitability into discrete classes (e.g. low, medium, high)
- Generation of cartographic outputs and summary statistics

---

## Why This Analysis Matters
This type of land suitability analysis supports:

- Evidence-based municipal land-use planning
- Identification of priority areas for agricultural or rural development
- Reduction of environmental and logistical risks
- Transparent and reproducible spatial decision-making
- Communication of complex spatial information to non-technical stakeholders

---

## Outputs
- Continuous land suitability raster (GeoTIFF)
- Classified suitability map
- Spatial statistics per suitability class
- Publication-ready cartographic outputs

---

## Project Structure
```text
Land_suitability/
│
├─ src/                  # Source code
│   ├─ preprocessing/
│   ├─ suitability/
│   └─ utils/
│
├─ data/                 # Input datasets
│   ├─ raw/
│   └─ processed/
│
├─ outputs/              # Results
│   ├─ rasters/
│   ├─ maps/
│   └─ tables/
│
├─ config/               # Configuration files (weights, rules)
├─ README.md
├─ requirements.txt
└─ .gitignore

---

## Reproducibility and Adaptability
This project is fully reproducible.  
All dependencies are managed through a virtual environment and documented in `requirements.txt`.

---

## Tools and Technologies
- Python
- PyQGIS (QGIS Processing Framework)
- GeoPandas
- Rasterio
- NumPy
- Matplotlib

---

## Author
**Santiago Gallego**  
Geospatial Analyst | GIS & Spatial Data Science
