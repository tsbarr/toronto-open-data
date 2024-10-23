# Toronto Pet Names Analysis 🐱🐕

An analysis of licensed pet names in Toronto from 2012-2022, demonstrating data processing with Python and visualization with Tableau Public.

## Project Overview

This analysis explores trends in pet names using Toronto's Open Data Portal, revealing how pet naming conventions have evolved over a decade in Canada's largest city. It showcases:
- Data acquisition through Toronto's CKAN API
- Data wrangling with pandas
- Interactive visualization with Tableau Public
- Time series analysis techniques

## Key Features

The analysis reveals several interesting patterns:
- Most popular names over time (e.g., "Charlie" maintaining popularity for dogs)
- Comparison between cat and dog naming trends
- The decline in "No Name" registrations for cats
- Emergence of new popular names (e.g., "Luna" rising in popularity)
- Total number of licensed pets by species
- Percentage of unique names over time

## Technical Implementation

### Data Pipeline
```python
# Core libraries
import requests
import pandas as pd

# API interaction
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
package_name = "licensed-dog-and-cat-names"

# Data processing highlights
- Standardization of "NO NAME" variants
- Year and species extraction from resource titles
- Rank calculation within year/species groups
```

### Data Processing Steps
1. API data retrieval from multiple yearly resources
2. Standardization of missing name values
3. Aggregation of counts by year, species, and name
4. Rank calculation for popularity analysis
5. Export to CSV for Tableau visualization

## Visualization

The Tableau dashboard includes three main views:
1. Top Names View - Tracks popularity of names over time
2. General Statistics - Shows total pets licensed and naming trends
3. Name Search - Allows exploration of specific name patterns

[Interactive Dashboard](https://public.tableau.com/app/profile/tsbarr/viz/Book2_17285038338800/PetNamesLicensedinToronto)

## Skills Demonstrated

- **Data Engineering**:
  - API interaction
  - Data cleaning and standardization
  - Complex data transformations
  
- **Analysis**:
  - Time series analysis
  - Comparative analysis
  - Pattern recognition

- **Visualization**:
  - Interactive dashboard design
  - Multi-view data presentation
  - User interface considerations

## Repository Structure

```
toronto-pet-names/
├── api_call_licensed_pets.ipynb   # Data acquisition and processing
├── Licensed_pets.csv              # Processed dataset
└── README.md                      # Project documentation
```

## Future Improvements

- Add breed analysis if data becomes available
- Implement automated data updates
- Add predictive modeling for name trends
- Create geographic visualization of pet names by neighborhood

## Tools Used

- Python 3.10
- pandas
- requests
- Tableau Public

## Running the Analysis

1. Clone the repository
2. Install requirements: `pip install pandas requests`
3. Run the Jupyter notebook
4. Open the CSV in Tableau to explore visualizations

---
*Part of a larger project exploring Toronto Open Data. Created during my transition from evolutionary biology to data science.*
