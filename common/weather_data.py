import requests
from pathlib import Path
from datetime import datetime
import time

def download_weather_data(
    station_id: int,
    start_year: int,
    start_month: int = 1,
    end_year: int = datetime.now().year,
    end_month: int = 12,
    output_dir: str = "weather_data"
) -> None:
    """
    Download historical weather data from Environment Canada.
    
    Args:
        station_id: The weather station ID
        start_year: Starting year for data collection
        end_year: Ending year for data collection
        output_dir: Directory to save downloaded files
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    base_url = (
        "https://climate.weather.gc.ca/climate_data/bulk_data_e.html"
    )
    
    # Common query parameters
    params = {
        "format": "csv",
        "stationID": station_id,
        "timeframe": 1,
        "submit": "Download+Data",
        "Day": 14  # Any day works as we're getting monthly data
    }
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # If first_year, 
            # skip months before start_month
            if year == start_year and month < start_month:
                continue
            # If last_year,
            # Break after end_month
            if year == end_year and month > end_month:
                break
            # Update parameters for this request
            params.update({"Year": year, "Month": month})
            
            try:
                # Make the request
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                
                # Get filename from content-disposition header or create one
                # if "content-disposition" in response.headers:
                #     filename = (
                #         response
                #         .headers["content-disposition"]
                #         .split("filename=")[1].strip('"')
                #     )
                # else:
                #     filename = f"weather_data_{station_id}_{year}_{month:02d}.csv"
                filename = f"weather_data_{station_id}_{year}_{month:02d}.csv"
                
                # Save the file
                output_path = Path(output_dir) / filename
                output_path.write_bytes(response.content)
                
                print(f"Downloaded data for {year}-{month:02d}")
                
                # Be nice to the server - add a small delay between requests
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {year}-{month:02d}: {e}")
                continue

if __name__ == "__main__":
    # Example usage for Toronto City Centre station (ID: 48549)
    download_weather_data(
        station_id=48549,
        start_year=2015,  # Match ferry data start year
        end_year=datetime.now().year
    )
