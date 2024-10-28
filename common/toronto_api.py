"""
toronto_api.py

Utilities for interacting with Toronto's Open Data CKAN API.
"""
import requests
import pandas as pd
from typing import Dict, List, Optional, Union
from datetime import datetime


class TorontoOpenDataAPI:
    """Client for interacting with Toronto's Open Data CKAN API."""
    
    def __init__(self):
        self.base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
        self.api_version = "3"
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the CKAN API.
        
        Args:
            endpoint: API endpoint (i.e., action to take; e.g., 'package_show')
            params: Dictionary of query parameters
            
        Returns:
            JSON response from the API
        """
        url = f"{self.base_url}/api/{self.api_version}/action/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    
    def get_package(self, package_name: str) -> Dict:
        """
        Get metadata for a specific package.
        
        Args:
            package_name: Name of the package (dataset)
            
        Returns:
            Package metadata result
        """
        package =  self._make_request("package_show", params={"id": package_name})
        if package.get('success'):
            return package.get('result')
        else: 
            error = package.get('error')
            raise Exception(
                f"{error.get('__type')} Error: {error.get('message')}"
            )
        
    def get_resource_csv(
            self,
            package_metadata: Dict
    ) -> pd.DataFrame:
        """

        Get data from a csv active resource.

        Args: 
            package_metadata: Dict containing metadata from a CKAN package.
        
        Returns:
            Dataframe with read csv

        """
        # Get the CSV resource
        try:

            csv_resource = next(
                (r for r in package_metadata['resources'] 
                    if r['format'] == 'CSV' 
                    and not r['datastore_active']
                ),
                None
            )
        except KeyError:
            print("Metadata incorrectly formatted (should contain a list of resources within a result)")
        except:
            print("Exception raised.")
        else:
            if csv_resource:
                df = pd.read_csv(csv_resource['url'])
                return df
            else:
                raise ValueError("No CSV resource found in package")
        
    
    def get_resource_data(
        self, 
        resource_id: str,
        format: str = 'csv'
    ) -> Union[pd.DataFrame, Dict]:
        """
        Get data from a specific resource.
        
        Args:
            resource_id: ID of the resource
            format: Desired format ('csv' or 'json')
            
        Returns:
            DataFrame for CSV resources, dictionary for JSON resources
        """
        if format.lower() == 'csv':
            return self.get_resource_csv("")
            # return pd.read_csv(
            #     f"{self.base_url}/dataset/{resource_id}/download"
            # )
        else:
            return self._make_request("datastore_search", 
                                    params={"id": resource_id})


class DataProcessor:
    """Common data processing utilities for Toronto Open Data."""
    
    @staticmethod
    def parse_datetime(
        df: pd.DataFrame,
        datetime_col: str,
        add_components: bool = True
    ) -> pd.DataFrame:
        """
        Parse datetime column and optionally add time components.
        
        Args:
            df: Input DataFrame
            datetime_col: Name of datetime column
            add_components: Whether to add year, month, day, hour columns
            
        Returns:
            DataFrame with processed datetime information
        """
        df = df.copy()
        df[datetime_col] = pd.to_datetime(df[datetime_col])
        
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


def get_example_usage():
    """Example usage of the utility classes."""
    # Initialize API client
    client = TorontoOpenDataAPI()
    
    # Get Ferry data
    ferry_package = client.get_package("toronto-island-ferry-ticket-counts")
    
    # Get the CSV resource
    for resource in ferry_package['result']['resources']:
        if resource['format'] == 'CSV':
            df = pd.read_csv(resource['url'])
            break
    
    # Process the data
    processor = DataProcessor()
    df = processor.parse_datetime(df, 'Timestamp')
    df = processor.add_temporal_flags(df, 'Timestamp')
    
    return df

if __name__ == "__main__":
    # Example usage
    df = get_example_usage()
    print("Data shape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    