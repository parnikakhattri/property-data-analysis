"""
Task 2: Property Analysis and Nearest Train Station Mapping

Background:
Real estate analytics often require integration of geospatial data, such as proximity to public transport, to enhance 
decision-making. Proximity to train stations is a critical factor influencing property value and buyer interest.

Purpose:
This script processes structured property and train station data, calculates the nearest train station for each property 
and saves the results into a JSON file for further analysis. It uses the haversine formula to calculate distances 
between geospatial coordinates.

Key Features:
1. Parses property and train station data from CSV files and converts them into dictionaries for analysis.
2. Calculates the distance between each property and all train stations using geospatial coordinates.
3. Identifies and returns the nearest train station for each property.
4. Outputs the results as a JSON file containing property IDs and their corresponding nearest station.

Inputs:
- Raw property data in CSV format, as defined in the configuration file (`PROPERTIES_FILE`).
  This file contains property details such as property ID, address, geolocation (latitude, longitude), 
  and other attributes.
- Train station data in CSV format, as defined in the configuration file (`STATIONS_FILE`).
  This file includes train station details such as station ID, name, and geolocation.

Outputs:
- A JSON file containing the nearest train station details for each property, as defined in the configuration 
  file (`NEAREST_STATION_OUTPUT`). The output includes the property ID and the nearest train station's name.

Usage:
1. Place the property data file (`PROPERTIES_FILE`) and train station data file (`STATIONS_FILE`) in the 
   specified paths in the configuration file.
2. Run the script to calculate distances and identify the nearest train station for each property:
   $ python task2_data_mapping.py
3. The results will be saved in the path specified by the `NEAREST_STATION_OUTPUT` configuration.

Functions:
1. `process_properties(file_name: str) -> dict`:
   - Processes the property data file and returns a dictionary of property details, indexed by property ID.

2. `process_stations(file_name: str) -> dict`:
   - Processes the train station data file and returns a dictionary of station details, indexed by station ID.

3. `nearest_station(properties: dict, stations: dict, prop_id: str) -> str`:
   - Finds and returns the name of the nearest train station for a given property.

4. `process_data() -> None`:
   - Main function that processes property and train station data, calculates the nearest station for each property,
     and saves the results to a JSON file.

Example Input:
1. Property data (`PROPERTIES_FILE`):
   prop_id,full_address,bedrooms,bathrooms,parking_spaces,latitude,longitude,land_area,floor_area,price
   P10001,3 Antrim Place Langwarrin VIC 3910,4,2,2,-38.16655678,145.1838435,608,257,870000

2. Train station data (`STATIONS_FILE`):
   stop_id,stop_name,stop_lat,stop_lon
   17204,Wallan Railway Station (Wallan),-37.416861,145.0053723

Example Output:
`NEAREST_STATION_OUTPUT`:
[
    {
        "property_id": "P10001",
        "nearest_station": "Wallan Railway Station (Wallan)"
    }
]
"""

import json
from utils.haversine import haversine_distance
from task1_data_parsing import extract_information
from utils.config import PROPERTIES_FILE, STATIONS_FILE, NEAREST_STATION_OUTPUT

def process_properties(file_name: str) -> dict:
    properties = {}
    with open(file_name, 'r') as file:
        next(file)  
        for line in file:
            property_info = extract_information(line.strip())
            if property_info['latitude'] and property_info['longitude']:
                properties[property_info['prop_id']] = property_info
    return properties


def process_stations(file_name: str) -> dict:
    stations = {}
    with open(file_name, 'r') as file:
        next(file)
        for line in file:
            stop_id, stop_name, stop_lat, stop_lon = line.strip().split(',')
            stations[stop_id] = {
                'stop_id': stop_id,
                'stop_name': stop_name,
                'stop_lat': float(stop_lat),
                'stop_lon': float(stop_lon)
            }
    return stations


def find_nearest_station(property_info: dict, stations: dict) -> dict:
    property_location = (property_info['latitude'], property_info['longitude'])
    nearest_station_name = None
    min_distance = float('inf')

    for station in stations.values():
        station_location = (station['stop_lat'], station['stop_lon'])
        distance = haversine_distance(
            property_location[0], property_location[1],
            station_location[0], station_location[1]
        )
        if distance < min_distance:
            min_distance = distance
            nearest_station_name = station['stop_name']

    return {
        "property_id": property_info['prop_id'],
        "nearest_station": nearest_station_name
    }


def process_data():
    properties = process_properties(PROPERTIES_FILE)
    stations = process_stations(STATIONS_FILE)

    results = []
    for prop_id, property_info in properties.items():
        nearest = find_nearest_station(property_info, stations)
        results.append(nearest)

    with open(NEAREST_STATION_OUTPUT, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Processed data saved to {NEAREST_STATION_OUTPUT}")


if __name__ == '__main__':
    process_data()
