import pandas as pd
import numpy as np

def identify_hierarchy_level(metric_name):
    """
    Determine hierarchy level based on leading spaces in metric name.
    
    Parameters:
    metric_name (str): Name of the metric
    
    Returns:
    int: Level in hierarchy (0 = top level)
    str: Clean metric name with spaces stripped
    """
    leading_spaces = len(metric_name) - len(metric_name.lstrip())
    return leading_spaces // 2, metric_name.strip()

import pandas as pd
import numpy as np

def identify_hierarchy_level(metric_name):
    """
    Determine hierarchy level based on leading spaces in metric name.
    
    Parameters:
    metric_name (str): Name of the metric
    
    Returns:
    int: Level in hierarchy (0 = top level)
    str: Clean metric name with spaces stripped
    """
    leading_spaces = len(metric_name) - len(metric_name.lstrip())
    return leading_spaces // 2, metric_name.strip()


def extract_hierarchical_metrics_names(df):
    """
    Extract metric names and their hierarchical relationships.
    
    Parameters:
    df (pd.DataFrame): Census data with first column as metric names
    
    Returns:
    Dictionary: metric hierarchies
    """
    
    # Create a dictionary to track metric hierarchies
    metric_hierarchy = {}
    current_0 = None
    current_1 = None
    
    # Process each row to understand the hierarchy
    for idx, row in df.iterrows():
        # get metric name from first column of row
        metric_name = row.iloc[0]
        # get tuple with level and name without spaces
        level, clean_name = identify_hierarchy_level(metric_name)
        # process it depending on level, up to level 2
        if level == 0:
            # new level 0 dict
            current_0 = clean_name
            metric_hierarchy[clean_name] = {}
        elif level == 1:
            # new level 1 dict
            current_1 = clean_name
            metric_hierarchy[current_0][clean_name] = []
        elif level == 2:
            # append to list
            metric_hierarchy[current_0][current_1].append(clean_name)
    
    return metric_hierarchy


def extract_population_metrics(df):
    """
    Extract metrics from census-formatted dataframe.
    
    Parameters:
    df (pd.DataFrame): Census data with first column as metric names
    
    Returns:
    pd.DataFrame: Processed population metrics by neighborhood
    tuple: Dictionary of metric hierarchies
    """
    # Get neighbourhood names (skip first column which is metric names)
    neighbourhoods = df.columns[1:]
    
    # Initialize results DataFrame
    results = pd.DataFrame(index=neighbourhoods)
    
    # Key metrics we want to extract with their parent categories
    target_metrics = {
        'total_population': 'Total - Age groups of the population - 25% sample data',
        # 'tsns_designation': 'TSNS 2020 Designation' # note: not numeric! if using, need to handle it in next loop
        # 'adults_15_64': '15 to 64 years',
        'youth_15_19': '15 to 19 years',
        'youth_20_24': '20 to 24 years',
        'seniors_65_plus': '65 years and over',
        'low_income': 'In low income based on the Low-income cut-offs, after tax (LICO-AT)',
        'median_income_2019': 'Median after-tax income in 2019 among recipients ($)',
        'median_income_2020': 'Median after-tax income in 2020 among recipients ($)'
    }
    
    # Extract each metric, considering hierarchy
    for result_name, metric_name in target_metrics.items():
        # Find the row with this metric, accounting for potential spaces
        metric_rows = df[df.iloc[:, 0].str.strip() == metric_name.strip()]
        
        if not metric_rows.empty:
            # Take the first matching row and convert to numeric
            metric_values = pd.to_numeric(
                metric_rows.iloc[0, 1:], 
                errors='coerce'
            )
            results[result_name] = metric_values
    
    # Calculate derived metrics
    if 'total_population' in results.columns:
        # Get total youths from both age groups
        results['youth_15_24'] = results['youth_15_19'] + results['youth_20_24']
        # results['adults_20_64'] = results['adults_15_64'] - results['youth_15_19']
        # Calculate percentages
        for col in ['youth_15_24', 'seniors_65_plus', 'low_income']:
            if col in results.columns:
                results[f'{col}_pct'] = (
                    results[col] / results['total_population'] * 100
                )
    
    # Reset index to make neighborhood a column
    results = results.reset_index()
    results = results.rename(columns={'index': 'neighborhood'})
    
    return results

# def calculate_service_need_index(population_df):
#     """
#     Calculate service need index considering hierarchical metrics.
    
#     Parameters:
#     population_df (pd.DataFrame): Processed population metrics
    
#     Returns:
#     pd.DataFrame: DataFrame with service need index
#     """
#     # Define weights for different factors
#     weights = {
#         'total_population': 0.15,
#         'youth_15_24_pct': 0.25,
#         'low_income_pct': 0.30,
#         'no_certificate_pct': 0.15,
#         'mental_health_risk': 0.15
#     }
    
#     # Normalize metrics
#     for col in weights.keys():
#         if col in population_df.columns:
#             if not col.endswith('_pct'):
#                 population_df[f'{col}_norm'] = (
#                     population_df[col] / population_df[col].max()
#                 )
#             else:
#                 # Percentage columns are already normalized
#                 population_df[f'{col}_norm'] = population_df[col] / 100
    
#     # Calculate weighted service need index
#     index_components = []
#     for metric, weight in weights.items():
#         norm_col = f'{metric}_norm'
#         if norm_col in population_df.columns:
#             index_components.append(weight * population_df[norm_col])
    
#     population_df['service_need_index'] = sum(index_components)
    
#     return population_df

# def analyze_neighborhoods(df, n_priorities=10):
#     """
#     Generate comprehensive neighborhood analysis.
    
#     Parameters:
#     df (pd.DataFrame): Raw census data
#     n_priorities (int): Number of priority neighborhoods to identify
    
#     Returns:
#     tuple: (metrics_df, priorities_df, summary_dict, hierarchy_dict)
#     """
#     # Extract metrics while preserving hierarchy
#     pop_metrics, hierarchy = extract_hierarchical_metrics(df)
    
#     # Calculate need index
#     pop_with_need = calculate_service_need_index(pop_metrics)
    
#     # Identify priority neighborhoods
#     priorities = (pop_with_need
#                  .sort_values('service_need_index', ascending=False)
#                  .head(n_priorities))
    
#     # Generate summary statistics
#     summary = {
#         'total_city_population': pop_metrics['total_population'].sum(),
#         'avg_neighborhood_pop': pop_metrics['total_population'].mean(),
#         'youth_proportion': (
#             pop_metrics['youth_15_24'].sum() / 
#             pop_metrics['total_population'].sum() * 100
#         ),
#         'low_income_proportion': (
#             pop_metrics['low_income'].sum() / 
#             pop_metrics['total_population'].sum() * 100
#         ),
#         'neighborhoods_analyzed': len(pop_metrics)
#     }
    
#     return pop_metrics, priorities, summary, hierarchy

# Example usage:
# df = pd.read_csv('nbhd_2021_census_profile_full_158model.csv')
# metrics, priorities, summary, hierarchy = analyze_neighborhoods(df)


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
