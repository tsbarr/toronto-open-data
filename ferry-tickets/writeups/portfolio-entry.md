# Toronto Ferry System Analysis: From Data to Insights

## Project Overview
An analysis of Toronto's Ferry system ticketing patterns from 2015-2024, revealing operational patterns and user behavior through data science techniques.

## Business Context
The Toronto Island Ferry service connects downtown Toronto with the Toronto Islands, serving both commuters and tourists. Understanding ticket sales and usage patterns is crucial for:
- Service optimization
- Resource allocation
- Revenue forecasting
- Customer experience improvement

## Technical Approach

### Data Processing Pipeline
```python
def analyze_ferry_patterns(df):
    """
    Key steps in data processing:
    1. Temporal feature engineering
    2. Multi-scale aggregation
    3. Pattern analysis
    """
    # Sample of actual implementation
    df['datetime'] = pd.to_datetime(df['Timestamp'])
    df['year'] = df['datetime'].dt.year
    
    # Aggregate at different time scales
    yearly = df.groupby('year').agg({
        'Sales Count': 'sum',
        'Redemption Count': 'sum'
    })
```

### Key Visualizations
Created three complementary views:
1. Yearly trends (bar chart)
2. Monthly seasonality (line plot)
3. Daily patterns (dual-line plot)

## Key Findings

### System Recovery & Resilience
- **COVID Impact**: ~70% reduction in volume during 2020
- **Recovery Pattern**: Steady increase post-2020
  - 2023 reached pre-pandemic levels
  - 2024 maintaining stable volumes
- **Insight**: System shows strong resilience to external shocks

### Seasonal Dynamics
- **Peak Season** (Summer):
  - Lower redemption/sales ratio (0.92 in June)
  - Indicates higher proportion of new ticket purchases
  - Suggests tourist-driven demand
  
- **Off Season** (Winter):
  - Higher redemption/sales ratio (1.19 in December)
  - Suggests prevalence of regular commuters
  - More efficient ticket utilization

### Daily Operating Patterns
- **Peak Hours**: 10:00-15:00
  - Maximum activity at 12:00 (noon)
  - Both sales and redemptions peak simultaneously
- **Evening Pattern**: 20:00-23:00
  - Sales exceed redemptions
  - Suggests advance purchasing for next-day use
- **Operational Implication**: Staffing needs vary significantly by time of day

## Business Recommendations

1. **Resource Optimization**
   - Adjust staffing levels based on daily patterns
   - Focus customer service during 10:00-15:00 peak
   - Consider reduced service during early morning hours

2. **Customer Experience**
   - Implement dynamic pricing for off-peak hours
   - Promote advance purchase during evening hours
   - Design different service levels for tourist vs. commuter seasons

3. **Revenue Enhancement**
   - Develop targeted pass options for regular commuters
   - Consider seasonal pricing strategies
   - Optimize ticket types based on usage patterns

## Technical Skills Demonstrated
- Data cleaning and preprocessing
- Time series analysis
- Statistical pattern recognition
- Data visualization
- Python programming (pandas, matplotlib, seaborn)
- Business insight extraction

## Future Improvements
1. Integration with weather data
2. Predictive modeling for demand forecasting
3. Analysis of special event impacts
4. Geographic analysis of user patterns

## Impact
This analysis provides actionable insights for:
- Operations planning
- Resource allocation
- Customer service improvement
- Revenue optimization

The findings can help the ferry service better serve its ~1.4 million annual passengers while optimizing operational efficiency.

---
*Note: This analysis was conducted using public data from the City of Toronto Open Data Portal. Code available on GitHub.*
