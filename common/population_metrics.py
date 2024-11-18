import pandas as pd
import numpy as np

def extract_population_metrics(df):
    """
    Extract key population metrics from census-format data 
    where metrics are rows and neighbourhoods are columns.
    
    Parameters:
    df (pd.DataFrame): Raw neighbourhood profile data where 
    columns are neighbourhoods and rows are metrics
    
    Returns:
    pd.DataFrame: Processed population metrics by neighbourhood
    """
    # First, get neighbourhood names (skip first column which is metric names)
    neighbourhoods = df.columns[1:]
    
    # Create a dictionary to store metric row indices
    metric_indices = {
        'total_pop': 'Total - Age groups of the population - 25% sample data',
        'youth_pop': '15 to 24 years',
        'adult_pop': '15 to 64 years',
        'senior_pop': '65 years and over',
        'median_income': 'Median total income in 2020 ($)',
        'low_income': ('In low income based on the Low-income measure, after tax (LIM-AT)')
    }
    
    # Initialize results DataFrame with neighbourhoods as index
    results = pd.DataFrame(index=neighbourhoods)
    
    # Extract each metric
    for metric_name, row_label in metric_indices.items():
        # Find the row with this metric
        metric_row = df.loc[df.iloc[:, 0] == row_label]
        if not metric_row.empty:
            # Add the metric values to results, converting to numeric
            results[metric_name] = pd.to_numeric(
                metric_row.iloc[0, 1:], 
                errors='coerce'
            )
    
    # Calculate derived metrics
    if 'total_pop' in results.columns and 'low_income' in results.columns:
        results['low_income_pct'] = (
            results['low_income'] / results['total_pop'] * 100
        )
    
    # Reset index to make neighbuorhood a column
    results = results.reset_index()
    results = results.rename(columns={'index': 'neighborhood'})
    
    return results

def calculate_service_need_index(population_df):
    """
    Calculate a service need index based on population characteristics.
    
    Parameters:
    population_df (pd.DataFrame): Processed population metrics
    
    Returns:
    pd.DataFrame: DataFrame with service need index
    """
    # Define weights for different factors
    weights = {
        'total_pop': 0.25,
        'youth_pop': 0.30,
        'low_income_pct': 0.45
    }
    
    # Create normalized versions of metrics
    for col in ['total_pop', 'youth_pop']:
        population_df[f'{col}_norm'] = (
            population_df[col] / population_df[col].max()
        )
    
    # Calculate weighted service need index
    population_df['service_need_index'] = (
        weights['total_pop'] * population_df['total_pop_norm'] +
        weights['youth_pop'] * population_df['youth_pop_norm'] +
        weights['low_income_pct'] * (population_df['low_income_pct'] / 100)
    )
    
    return population_df

def generate_neighborhood_report(df, n_priorities=10):
    """
    Generate a comprehensive neighborhood analysis report.
    
    Parameters:
    df (pd.DataFrame): Raw census data
    n_priorities (int): Number of priority neighborhoods to identify
    
    Returns:
    tuple: (population_metrics, priority_neighborhoods, summary_stats)
    """
    # Extract base metrics
    pop_metrics = extract_population_metrics(df)
    
    # Calculate need index
    pop_with_need = calculate_service_need_index(pop_metrics)
    
    # Get priority neighborhoods
    priorities = (pop_with_need
                 .sort_values('service_need_index', ascending=False)
                 .head(n_priorities))
    
    # Calculate summary statistics
    summary_stats = {
        'total_population': pop_metrics['total_pop'].sum(),
        'avg_neighborhood_pop': pop_metrics['total_pop'].mean(),
        'avg_low_income_pct': pop_metrics['low_income_pct'].mean(),
        'median_youth_pop': pop_metrics['youth_pop'].median()
    }
    
    return pop_metrics, priorities, summary_stats

# Example usage:
# df = pd.read_csv('nbhd_2021_census_profile_full_158model.csv')
# pop_metrics, priorities, summary = generate_neighborhood_report(df)
# 
# print("\nPriority Neighborhoods for Mental Health Services:")
# print(priorities[['neighborhood', 'service_need_index', 'total_pop', 
#                  'youth_pop', 'low_income_pct']])
