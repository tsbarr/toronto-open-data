"""
toronto_api.py

Utilities for interacting with Toronto's Open Data CKAN API.
"""
import requests
import pandas as pd
from typing import Dict, List, Optional, Union, Callable
from datetime import datetime
from data_processors import DataProcessor


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
        
    def show_resources_info(
            self,
            package_metadata: Dict
    ) -> None:
        """

        Print info of resources in package.

        Args: 
            package_metadata: Dict containing metadata from a CKAN package.
        
        
        Return: 
            None. Function only prints the info and returns nothing.
            Info printed: Number of resources in the package, 
            their name, format, url_type and 
            if they are datastore_active
        
        """
        # Check resources in package using metadata
        print(f'Number of resources: {package_metadata["num_resources"]}\n')
        for idx, resource in enumerate(package_metadata["resources"]):
            print(f'''\
{idx}: {resource["name"]}
    datastore_active: {resource['datastore_active']}
    format: {resource['format']}
    url_type: {resource['url_type']}
            ''')

    def get_resource_datastore(
            self,
            package_metadata: Dict
    ) -> pd.DataFrame:
        """

        Get data from an active datastore resource.

        Args: 
            package_metadata: Dict containing metadata from a CKAN package.
        
        Returns:
            Dataframe with read data

        """
        # Get the active datastore resource
        try:
            resource = next(
                (r for r in package_metadata['resources'] 
                    if (r['datastore_active'])
                ),
                None
            )
        except KeyError:
            print("Metadata incorrectly formatted (should contain a list of resources within a result)")
        except:
            print("Exception raised.")
        else:
            if resource:
                df = pd.read_csv(resource['url'])
                return df
            else:
                raise ValueError("No active datastore found in package")

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
        # resource_id: str,
        package_metadata: Dict,
        format: str = 'datastore'
    ) -> Union[pd.DataFrame, Dict]:
        """
        Get data from a specific resource.
        
        Args:
            # resource_id: ID of the resource
            package_metadata: Dict containing metadata from a CKAN package.
            format: Source format ('datastore', 'csv' or 'json')
            
        Returns:
            DataFrame for datastore and CSV resources, dictionary for JSON resources
        """
        if format.lower() == 'datastore':
            return self.get_resource_datastore(package_metadata)
        if format.lower() == 'csv':
            return self.get_resource_csv(package_metadata)
            # return pd.read_csv(
            #     f"{self.base_url}/dataset/{resource_id}/download"
            # )
        # TODO: implement json format
        else:
            print('incorrect or unimplemented format')
            return package_metadata
            # return self._make_request("datastore_search", 
            #                         params={"id": resource_id})

    # def get_resource_data(
    #     self,
    #     resource: Dict,
    #     preprocessor: Optional[Callable] = None,
    #     **kwargs
    # ) -> pd.DataFrame:
    #     """
    #     Get data from a resource, handling different file formats.
        
    #     Args:
    #         resource: Resource dictionary from package metadata
    #         preprocessor: Optional function to preprocess the data
    #         **kwargs: Additional arguments for read functions
            
    #     Returns:
    #         Processed DataFrame
    #     """
    #     file_format = resource.get('format', '').lower()
        
    #     if file_format == 'csv':
    #         df = pd.read_csv(resource['url'], **kwargs)
    #     elif file_format in ['xls', 'xlsx']:
    #         df = pd.read_excel(resource['url'], **kwargs)
    #     else:
    #         raise ValueError(f"Unsupported file format: {file_format}")
            
    #     if preprocessor:
    #         df = preprocessor(df, resource)
            
    #     return df





def get_example_usage():
    """Example usage of the utility classes."""
    # Initialize API client
    client = TorontoOpenDataAPI()
    
    # Get Ferry data
    ferry_package = client.get_package("toronto-island-ferry-ticket-counts")
    
    # Get the CSV resource
    for resource in ferry_package['resources']:
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
    print('\n', df.head())
    