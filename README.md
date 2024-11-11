# Toronto Open Data Analysis

## Overview
This repository contains analyses of various public datasets from the [City of Toronto's Open Data Portal](https://open.toronto.ca/). Each analysis explores different aspects of urban life and city services, combining data science techniques with a focus on community impact.

## Motivation
As a data scientist transitioning from evolutionary biology research, I'm fascinated by patterns in urban systems just as I once studied patterns in natural systems. Cities generate rich datasets that can help us understand and improve urban life. Toronto, my home city, provides extensive open data that enables evidence-based insights into how our city works and how we might make it better.

## Projects

### 🏥 [Mental Health Services Analysis](mental-health-services)
Analyzing Toronto's mental health infrastructure (2014-2024) to understand:
- Geographic distribution of mental health services
- Patterns in crisis response and apprehensions
- Relationship between service availability and crisis events
- Spatial equity in mental health resource distribution

### 🚢 [Ferry Service Analysis](ferry_tickets)
Analyzing patterns in Toronto Island Ferry usage to understand:
- Seasonal and daily transit patterns
- Impact of weather and events on ridership
- Opportunities for service optimization

### 🐱🐕 [Pet Names Analysis](licensed-pets)
Exploring a decade of Toronto's pet licensing data (2012-2022) to reveal:
- Evolution of pet naming trends
- Comparative analysis between cat and dog names
- Time series analysis of name popularity
- Interactive visualizations of naming patterns

## Technical Stack
- **Data Collection**: Python, CKAN API
- **Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Tableau
- **Documentation**: Jupyter Notebooks, Markdown

## Repository Structure
```
toronto-open-data/
├── mental-health-services/   # Mental Health Services analysis
├── ferry_tickets/            # Toronto Island Ferry analysis
├── licensed-pets/            # Pet Names analysis
└── common/                   # Shared utilities and helpers
    ├── utils.py              # Common functions
    ├── toronto_api.py        # API interaction tools
    └── weather.py            # Weather data tools
```
<!-- └── docs/              # Additional documentation
``` -->

<!-- ## Getting Started
1. Clone this repository:
   ```bash
   git clone https://github.com/tsbarr/toronto-open-data.git
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Explore individual project directories for specific analyses -->

## Contributing
While this is a personal portfolio project, I welcome suggestions and discussions about:
- Additional datasets to analyze
- New analytical approaches
- Improvements to existing analyses
- Bug fixes

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- Tania Barrera
- [My website](taniabarrera.ca)
- [LinkedIn](https://www.linkedin.com/in/tania-sofia-barrera/)
- [Tableau Public](https://public.tableau.com/app/profile/tsbarr/vizzes)

## Acknowledgments
- City of Toronto Open Data Team
- Toronto's data science community
