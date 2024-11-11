# Toronto Mental Health Services Analysis 🏥

## Overview
An analysis of Toronto's mental health services infrastructure and crisis response patterns from 2014-2024, exploring the spatial relationship between service availability and Mental Health Act apprehensions across neighborhoods.

## Project Context
This analysis combines multiple public health datasets to understand:
- Geographic distribution of mental health services
- Patterns in crisis response (Mental Health Act apprehensions)
- Relationship between service availability and crisis events
- Temporal trends in mental health-related incidents

## Data Sources
- **Mental Health Services**: 99 service locations
  - General mental health services
  - Concurrent disorder programs
- **Crisis Events**: 112,314 Mental Health Act apprehensions (2014-2024)
- **Geographic Data**: Toronto neighborhood boundaries

## Technical Implementation

### Data Pipeline

```python
# Core components
import pandas as pd
import geojson
from datetime import datetime
```

### Data processing workflow:
1. API connection to Toronto Open Data Portal
2. Data cleaning and standardization
3. Geographic coordinate extraction
4. Temporal feature engineering
5. Spatial joins and aggregations


### Analysis Features
- Spatial distribution analysis of services
- Temporal pattern recognition in crisis events
- Service density calculations by neighborhood
- Geographic visualization with Mapbox integration
- Interactive filtering by year and service type

## Key Findings

### Service Distribution
- Concentration in downtown core (particularly Church-Yonge Corridor)
- Limited coverage in outer regions
- Distinct patterns between general services and specialized programs

### Crisis Response Patterns
- Temporal trends in apprehension events
- Geographic hotspots
- Relationship between service proximity and incident frequency

## Visualization
Interactive dashboard featuring:
1. Choropleth map of apprehension density
2. Service location overlay with type distinction
3. Time-series analysis capabilities
4. Neighborhood-level statistics

## Technical Skills Demonstrated
- **Data Engineering**:
  - API interaction
  - Geographic data processing
  - Complex data transformations
- **Analysis**:
  - Spatial analysis
  - Time series analysis
  - Pattern recognition
- **Visualization**:
  - Interactive mapping
  - Multi-layer visualization
  - User interface design

## Future Improvements
1. Integration with demographic data
2. Predictive modeling for service placement
3. Automated data refresh pipeline
4. Enhanced visualization features

## Tools Used
- Python 3.10
- pandas & geojson
- Tableau Public
- Toronto Open Data API

## Repository Structure
```
toronto-mental-health/
├── data/
│   ├── raw/          # Original datasets
│   └── processed/    # Cleaned data files
├── notebooks/
│   ├── 01_data_collection.ipynb
│   └── 02_analysis.ipynb
└── README.md
```

## Running the Analysis
1. Clone this repository
2. Install requirements: `pip install pandas geojson`
3. Run the Jupyter notebooks in sequence
4. View the Tableau dashboard [link](https://public.tableau.com/app/profile/tsbarr/viz/TorontoNeighbourhoodsMentalHealthApprehensionsandServices/MentalHealthServicesandCrisisResponseDistribution?publish=yes)

---
*Part of a portfolio demonstrating data science applications in public health and urban planning. Created during my transition from evolutionary biology research to data science.*
