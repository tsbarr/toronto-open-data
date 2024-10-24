"""
utils.py

General utility functions for data analysis projects.
"""
import pandas as pd
import numpy as np
from typing import List, Optional
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_rolling_stats(
    df: pd.DataFrame,
    value_col: str,
    window: int = 7,
    group_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate rolling statistics for a time series.
    
    Args:
        df: Input DataFrame
        value_col: Column containing values to analyze
        window: Rolling window size
        group_cols: Columns to group by before calculating stats
        
    Returns:
        DataFrame with rolling statistics added
    """
    df = df.copy()
    
    if group_cols:
        df = df.sort_values(group_cols + [value_col])
        grouped = df.groupby(group_cols)
        
        df[f'{value_col}_rolling_mean'] = (
            grouped[value_col].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
        )
        df[f'{value_col}_rolling_std'] = (
            grouped[value_col].transform(
                lambda x: x.rolling(window, min_periods=1).std()
            )
        )
    else:
        df = df.sort_values(value_col)
        df[f'{value_col}_rolling_mean'] = (
            df[value_col].rolling(window, min_periods=1).mean()
        )
        df[f'{value_col}_rolling_std'] = (
            df[value_col].rolling(window, min_periods=1).std()
        )
    
    return df


def plot_time_patterns(
    df: pd.DataFrame,
    datetime_col: str,
    value_col: str,
    agg_freq: str = 'D',
    title: Optional[str] = None
) -> None:
    """
    Create a time series plot with patterns highlighted.
    
    Args:
        df: Input DataFrame
        datetime_col: Name of datetime column
        value_col: Column to plot
        agg_freq: Frequency for resampling ('D' for daily, 'W' for weekly, etc)
        title: Plot title
    """
    # Resample data
    resampled = (
        df.set_index(datetime_col)
        .resample(agg_freq)[value_col]
        .mean()
        .reset_index()
    )
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot raw data and rolling average
    sns.scatterplot(
        data=resampled,
        x=datetime_col,
        y=value_col,
        alpha=0.5,
        label='Raw data'
    )
    
    sns.lineplot(
        data=resampled,
        x=datetime_col,
        y=value_col,
        color='red',
        label='Trend',
        alpha=0.8
    )
    
    # Customize plot
    plt.title(title or f'{value_col} over time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    

def detect_outliers(
    df: pd.DataFrame,
    value_col: str,
    n_std: float = 3.0
) -> pd.Series:
    """
    Detect outliers using z-score method.
    
    Args:
        df: Input DataFrame
        value_col: Column to check for outliers
        n_std: Number of standard deviations for threshold
        
    Returns:
        Boolean series indicating outliers
    """
    z_scores = np.abs(
        (df[value_col] - df[value_col].mean()) / 
        df[value_col].std()
        )
    return z_scores > n_std
