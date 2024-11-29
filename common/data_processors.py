"""
data_processors.py

Common data processing utilities for Toronto Open Data.

"""

import pandas as pd
from typing import Dict
from datetime import datetime

class DataProcessor:
    
    @staticmethod
    def parse_datetime(
        df: pd.DataFrame,
        datetime_col: str,
        add_components: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Parse datetime column and optionally add time components.
        
        Args:
            df: Input DataFrame
            datetime_col: Name of datetime column
            add_components: Whether to add year, month, day, hour columns
            **kwargs: Additional arguments for to_datetime function
            
        Returns:
            DataFrame with processed datetime information
        """
        df = df.copy()
        df[datetime_col] = pd.to_datetime(df[datetime_col], **kwargs)
        
        if add_components:
            df[f'{datetime_col}_year'] = df[datetime_col].dt.year
            df[f'{datetime_col}_month'] = df[datetime_col].dt.month
            df[f'{datetime_col}_day'] = df[datetime_col].dt.day
            df[f'{datetime_col}_hour'] = df[datetime_col].dt.hour
            df[f'{datetime_col}_dayofweek'] = df[datetime_col].dt.dayofweek
            
        return df
    
    @staticmethod
    def add_temporal_flags(
        df: pd.DataFrame,
        datetime_col: str
    ) -> pd.DataFrame:
        """
        Add useful temporal flags to the DataFrame.
        
        Args:
            df: Input DataFrame
            datetime_col: Name of datetime column
            
        Returns:
            DataFrame with additional temporal flags
        """
        df = df.copy()
        
        # Get today's date and latest date in data
        today = datetime.today().date()
        latest = df[datetime_col].dt.date.max()
        
        # Add flags
        df['is_weekend'] = df[datetime_col].dt.dayofweek >= 5
        df['is_today'] = df[datetime_col].dt.date == today
        df['is_latest'] = df[datetime_col].dt.date == latest
        
        return df


class FerryDataProcessor:
    """Processor for ferry data."""
    @staticmethod
    def process_resource(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Process ferry ticket data."""
        df = df.copy()
        df = DataProcessor.parse_datetime(
            df,
            datetime_col='Timestamp',
            add_components=False,
            format='%Y-%m-%dT%H:%M:%S'
        )
        df = DataProcessor.add_temporal_flags(df, 'Timestamp')
        # # Parse Timestamp as datetime obj
        # df['datetimeTimestamp'] = pd.to_datetime(
        #     df['Timestamp'],
        #     format="%Y-%m-%dT%H:%M:%S"
        # )

        # # Get latest date
        # latest = max(df['datetimeTimestamp']).date()
        # print(f"latest:\t{latest}")
        # # Get today's date
        # today = datetime.today().date()
        # print(f"today:\t{today}")

        # # Checking if the date part of timestamp is the same as today and latest date, add as df columns
        # df['isToday'] = today == df['datetimeTimestamp'].dt.date
        # df['isLatest'] = latest == df['datetimeTimestamp'].dt.date
        
        return df
    
class PetNamesProcessor:
    """Processor for pet names data."""
    
    def __init__(self):
        self.no_name_values = ['', 'N/A', 'NO NAME LISTED']
        
    def process_resource(
        self,
        df: pd.DataFrame,
        resource: Dict
    ) -> pd.DataFrame:
        """Process a single pet names resource."""
        # Clean and standardize names
        df = df.copy()
        df.columns = ['name', 'count']
        
        # Standardize NO NAME entries and clean counts
        df['name'] = df['name'].apply(
            lambda x: 'NO NAME' if x in self.no_name_values else x
        )
        df['count'] = pd.to_numeric(
            df['count'].replace('', 0), 
            errors='coerce'
        ).fillna(0)
        
        # Extract year and species from resource name
        title = resource['name'].strip('\t').split('-')
        df['year'] = title[-1]
        df['species'] = title[-2].strip('s')
        
        # Filter out empty rows
        df = df[df['count'] > 0]
        
        return df
    
    def post_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Post-process the complete dataset."""
        # Convert count to integer
        df['count'] = df['count'].astype('Int64')
        
        # Group by year, species, name and calculate totals
        df = (df
            .groupby(['year', 'species', 'name'], as_index=False)
            .sum()
            .sort_values(
                by=[
                    'year',
                    'species',
                    'count'
                ],
                ascending=[
                    True,
                    True,
                    False
                ]
            )
        )
        
        # Calculate rank within year and species
        df['rank'] = (df
            .drop(columns='name')
            .groupby(['year', 'species'])
            .rank(method='min', ascending=False)
        )
        
        return df
