# Toronto Island Ferry Analysis

## Overview
This analysis explores patterns in Toronto Island Ferry usage, providing insights into urban mobility and recreational behavior. Using data from the City of Toronto's Open Data Portal, I analyze ticket sales and redemption patterns to understand service usage and suggest potential optimizations.

## Key Questions
- What are the dominant temporal patterns in ferry usage?
- How do weather and events impact ridership?
- Can we identify opportunities for service optimization?
- What insights might help improve the user experience?

## Data Source
Data is collected from the [Toronto Island Ferry Ticket Counts](https://open.toronto.ca/dataset/toronto-island-ferry-ticket-counts/) dataset, which provides:
- 15-minute interval ticket sales and redemptions
- Historical data from 2015 to present
- Real-time updates via CKAN API

## Key Findings
1. **Seasonal Patterns**
   - Summer ridership 3x higher than winter months
   - Weekend peaks reach 200% of weekday traffic
   - Special events create significant usage spikes

2. **Daily Patterns**
   - Weekday peaks: 8:00-9:30 AM, 4:30-6:00 PM
   - Weekend peaks: 11:00 AM - 3:00 PM
   - Weather impacts weekend ridership more than weekday
<!-- 
## Repository Structure
```
ferry-analysis/
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_pattern_analysis.ipynb
├── src/
│   ├── data_collection.py
│   └── analysis_utils.py
├── data/
│   └── processed/
├── blog/
│   └── analysis_blog_post.md
├── requirements.txt
└── README.md
```

## Technical Implementation
- Python pipeline for API data collection
- Pandas for time series analysis
- Statistical analysis of usage patterns
- Visualization using Matplotlib/Seaborn

## Getting Started
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run Jupyter notebooks in order:
   ```bash
   jupyter notebook notebooks/01_data_collection.ipynb
   ``` -->

## Tableau dashboard
Explore the current state of the analysis via the [interactive dashboard](https://public.tableau.com/app/profile/tsbarr/viz/TorontoFerryTicketSales_17206436740190/TorontoIslandFerry) I published in Tableau Public.

## Future Improvements
- [ ] Add YoY KPIs to interactive dashboard
- [ ] Weather data integration
- [ ] Predictive modeling for demand
- [ ] Automated anomaly detection


## Blog Post
For a detailed discussion of the analysis and findings, see the [draft blog post](./blog.md).

## Dependencies
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- requests
- jupyter

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
