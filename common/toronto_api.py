"""
toronto_api.py

Utilities for interacting with Toronto's Open Data CKAN API.
"""

import requests
import pandas as pd
from typing import Dict, Optional

class TorontoOpenDataAPI:
    """Client for interacting with Toronto's Open Data CKAN API."""
    
    def __init__(self, package_name):
        self.base_url = 'https://ckan0.cf.opendata.inter.prod-toronto.ca'
        self.api_version = '3'
        self.package_metadata = self.get_package(package_name)
    
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
            self
    ):
        """

        Print info of resources in package.
        
        Return: 
            None. Function only prints the info and returns nothing.
            Info printed: Number of resources in the package, 
            their name, format, url_type and 
            if they are datastore_active
        
        """
        # Check resources in package using metadata
        print(f"Number of resources: {self.package_metadata['num_resources']}\n")
        for resource in self.package_metadata['resources']:
            print(f"""{resource['position']}: {resource['name']}
    datastore_active: {resource['datastore_active']}
    format: {resource['format']}
    url_type: {resource['url_type']}
            """)

    def get_resource_data(
        self,
        resource_idx: int = 0,
        **kwargs
    ) -> pd.DataFrame:
        """
        Get data from a resource, handling different file formats.
        
        Args:
            resource_idx: idx of desired resource within the package metadata, defaults to first position (0)
            **kwargs: Additional arguments for read functions
            
        Returns:
            Processed DataFrame
        """
        # Get the desired resource metadata
        try:
            resource = next(
                (r for r in self.package_metadata['resources'] 
                    if (r['position'] == resource_idx)
                ),
                None
            )
        except KeyError:
            print("Metadata incorrectly formatted (should contain a list of resources within a result, each with a 'position' value.)")
        except:
            print("Exception raised.")
        file_format = resource.get('format', '').lower()
        
        if file_format == 'csv':
            df = pd.read_csv(resource['url'], **kwargs)
        elif file_format in ['xls', 'xlsx', 'excel']:
            df = pd.read_excel(resource['url'], **kwargs)
        elif file_format in ['xml']:
            df = pd.read_xml(resource['url'], **kwargs)
        elif file_format in ['json']:
            df = pd.read_json(resource['url'], **kwargs)
        else:
            raise ValueError(f'Unsupported file format: {file_format}')
            
        return df
