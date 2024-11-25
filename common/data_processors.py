"""
data_processors.py

Data processors used to process dataframes resulting from 
Toronto's Open Data CKAN API resource calls.
"""
import pandas as pd
from typing import Dict

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


class FerryDataProcessor:
    """Processor for ferry data."""
    
    def process_resource(
        self,
        df: pd.DataFrame,
        resource: Dict
    ) -> pd.DataFrame:
        """Process ferry ticket data."""
        df = df.copy()
        
        # Parse datetime
        df['datetimeTimestamp'] = pd.to_datetime(
            df['Timestamp'],
            format="%Y-%m-%dT%H:%M:%S"
        )
        
        # Add temporal components
        df['year'] = df['datetimeTimestamp'].dt.year
        df['month'] = df['datetimeTimestamp'].dt.month
        df['day'] = df['datetimeTimestamp'].dt.day
        df['hour'] = df['datetimeTimestamp'].dt.hour
        df['dayofweek'] = df['datetimeTimestamp'].dt.dayofweek
        
        return df
