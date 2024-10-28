import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns


# ---
# Redemption/Sales ratio
# ---

def analyze_ferry_patterns(df):
    """
    Analyze ferry ticket sales vs redemptions across different time scales.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with columns for Timestamp, Sales Count,
    and Redemption Count
    
    Returns:
    dict: Dictionary containing analysis results at different time scales
    """
    # Ensure timestamp is datetime
    df['datetime'] = pd.to_datetime(df['Timestamp'])
    
    # Add time components
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    
    # Calculate differences at various time scales
    # Dict to store results
    analyses = {}
    
    # Yearly analysis
    yearly = (
        df
        .groupby('year')
        .agg({
            'Sales Count': 'sum',
            'Redemption Count': 'sum'
        })
        .assign(
            difference=lambda x: (
            x['Redemption Count'] - x['Sales Count']
            ),
            ratio=lambda x: (
                x['Redemption Count'] / x['Sales Count']
            )
        ))
    analyses['yearly'] = yearly
    
    # Monthly analysis
    monthly = (
        df
        .groupby(['year', 'month'])
        .agg({
            'Sales Count': 'sum',
            'Redemption Count': 'sum'
        })
        .assign(
            difference=lambda x: (
            x['Redemption Count'] - x['Sales Count']
            ),
            ratio=lambda x: (
            x['Redemption Count'] / x['Sales Count']
            )
        ))
    analyses['monthly'] = monthly
    
    # Hourly patterns
    hourly = (
        df
        .groupby('hour')
        .agg({
        'Sales Count': 'mean',
        'Redemption Count': 'mean'
        })
        .assign(
            difference=lambda x: (
                x['Redemption Count'] - x['Sales Count']
            ),
            ratio=lambda x: (
                x['Redemption Count'] / x['Sales Count']
            )
        ))
    analyses['hourly'] = hourly
    
    return analyses

def plot_patterns(analyses):
    """
    Create visualizations of ferry ticket patterns.
    
    Parameters:
    analyses (dict): Output from analyze_ferry_patterns function
    """
    # Set style
    plt.style.use('seaborn-v0_8')
    
    # Create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
    
    # Yearly patterns
    yearly = analyses['yearly']
    yearly[['Sales Count', 'Redemption Count']].plot(
        kind='bar',
        ax=ax1,
        width=0.8
    )
    ax1.set_title('Yearly Ticket Patterns')
    ax1.set_ylabel('Count')
    ax1.tick_params(axis='x', rotation=45)
    
    # Monthly ratio pattern
    monthly = analyses['monthly']
    monthly_avg = (monthly
        .groupby('month')['ratio'].mean().reset_index())
    sns.lineplot(
        data=monthly_avg,
        x='month',
        y='ratio',
        ax=ax2,
        marker='o'
    )
    ax2.set_title('Average Monthly Redemption/Sales Ratio')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Ratio')
    
    # Hourly pattern
    hourly = analyses['hourly']
    hourly[['Sales Count', 'Redemption Count']].plot(
        kind='line',
        ax=ax3,
        marker='o'
    )
    ax3.set_title('Average Hourly Patterns')
    ax3.set_xlabel('Hour of Day')
    ax3.set_ylabel('Average Count')
    
    plt.tight_layout()
    return fig

def generate_insights(analyses):
    """
    Generate key insights from the analyses.
    
    Parameters:
    analyses (dict): Output from analyze_ferry_patterns function
    
    Returns:
    dict: Dictionary containing key insights
    """
    yearly = analyses['yearly']
    monthly = analyses['monthly']
    hourly = analyses['hourly']
    
    insights = {
        'years_with_excess_redemptions': (
            yearly[yearly['difference'] > 0].index.tolist()
        ),
        'max_redemption_ratio': {
            'value': yearly['ratio'].max(),
            'year': yearly['ratio'].idxmax()
        },
        'avg_monthly_ratio': monthly['ratio'].mean(),
        'peak_hour': {
            'redemptions': hourly['Redemption Count'].idxmax(),
            'sales': hourly['Sales Count'].idxmax()
        }
    }
    
    return insights

#  ---
# KPIs
#  ---

def analyze_ferry_service_kpis(df):
    """
    Calculate key performance indicators for ferry service optimization.
    
    Parameters:
    df: pandas DataFrame with columns ['Timestamp', 'Sales Count', 
        'Redemption Count']
    
    Returns:
    dict: KPIs and metrics for operational decision making
    """
    # Create datetime index
    df['datetime'] = pd.to_datetime(df['Timestamp'])
    df.set_index('datetime', inplace=True)
    
    # Calculate hourly and daily aggregations
    hourly_data = df.resample('H').sum()
    daily_data = df.resample('D').sum()
    
    # Calculate service utilization rate
    utilization = (df['Redemption Count'] / df['Sales Count']).mean() * 100
    
    # Calculate peak hours (top 10% of traffic hours)
    peak_threshold = np.percentile(
        hourly_data['Redemption Count'], 
        90
    )
    peak_hours = hourly_data[
        hourly_data['Redemption Count'] >= peak_threshold
    ].index.hour.value_counts()
    
    # Calculate week-over-week growth
    weekly_data = daily_data.resample('W').sum()
    wow_growth = (
        (weekly_data - weekly_data.shift(1)) / weekly_data.shift(1) * 100
    )
    
    # Calculate ticket efficiency (unused tickets)
    unused_rate = (
        (df['Sales Count'] - df['Redemption Count']).sum() / 
        df['Sales Count'].sum() * 100
    )
    
    # Prepare KPI dictionary
    kpis = {
        'service_utilization_rate': round(utilization, 2),
        'peak_service_hours': peak_hours.index.tolist()[:3],
        'avg_weekly_growth_rate': round(wow_growth['Sales Count'].mean(), 2),
        'unused_ticket_rate': round(unused_rate, 2),
        'daily_capacity_stats': {
            'avg_daily_passengers': int(daily_data['Redemption Count'].mean()),
            'max_daily_capacity': int(daily_data['Redemption Count'].max()),
            'min_daily_capacity': int(daily_data['Redemption Count'].min())
        }
    }
    
    return kpis
