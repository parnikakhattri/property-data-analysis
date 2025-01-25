"""
Task 1: Data Extraction and Transformation 

Background:
Real estate agencies and analysts often receive raw, unstructured property data from various sources. 
This data, while valuable, requires significant processing to be usable for analysis or decision-making. 
For instance, key details such as property type, location, features and pricing may be incomplete, 
inconsistent or improperly formatted.

Purpose:
This script focuses on transforming raw property data strings into a clean, structured format. The 
extracted data includes key attributes such as:
- Property ID, type and address.
- Geolocation (latitude, longitude).
- Features like the number of bedrooms, bathrooms, parking spaces and additional amenities.

The script also provides utility functions to dynamically update a property's feature list by adding or 
removing specific features.

Key Features:
1. Parses raw property strings in CSV format and extracts key details into a well-structured dictionary.
2. Gracefully handles missing or incomplete data by defaulting to `None` or skipping invalid entries.
3. Includes utility functions to add or remove features dynamically from a property's feature list.
4. Outputs the processed data in a JSON format for downstream analysis.

Inputs:
- Raw property data in CSV format, as defined in the configuration file (`PROPERTIES_FILE`).

Outputs:
- Processed property data saved as a JSON file, as defined in the configuration file (`EXTRACTED_PROPERTIES`).

Usage:
1. Define the input and output file paths in the configuration file (`utils/config.py`).
2. Place the raw property data file in the appropriate directory as specified in the configuration.
3. Run this script to process the data:
   $ python src/task1_data_parsing.py
4. The cleaned data will be saved to the location specified in the configuration file.

Functions:
1. `extract_information(property_string: str) -> dict`:
   - Parses a raw property string in CSV format and extracts details such as property ID, address, geolocation, 
     and features.
   - Returns a structured dictionary containing the extracted property details.

2. `read_property_file(file_path: str) -> list`:
   - Reads property data from a file and returns a list of raw property strings for processing.

3. `save_to_json(data: list, output_path: str) -> None`:
   - Saves a list of processed property dictionaries to a JSON file.

4. `add_feature(property_dict: dict, feature: str) -> None`:
   - Dynamically adds a specified feature to the property's feature list, ensuring no duplicates.

5. `remove_feature(property_dict: dict, feature: str) -> None`:
   - Removes a specified feature from the property's feature list, if it exists.

Example Input:
A single property string in CSV format:
"P10001,3 Antrim Place Langwarrin VIC 3910,4,2,2,-38.16655678,145.1838435,,608,257,870000,dishwasher;central heating"

Example Output:
A dictionary containing structured property details:
{
    "prop_id": "P10001",
    "prop_type": "house",
    "full_address": "3 Antrim Place Langwarrin VIC 3910",
    "suburb": "Langwarrin",
    "bedrooms": 4,
    "bathrooms": 2,
    "parking_spaces": 2,
    "latitude": -38.16655678,
    "longitude": 145.1838435,
    "land_area": 608,
    "floor_area": 257,
    "price": 870000,
    "property_features": ["dishwasher", "central heating"]
}

Note:
- Fields such as `latitude`, `longitude`, or `features` will default to `None` or an empty list 
  if they are missing or invalid.
- The script ensures proper validation of latitude and longitude values to prevent erroneous data entry.
"""

import os
import json
from utils.config import PROPERTIES_FILE, EXTRACTED_PROPERTIES

def extract_information(property_string: str) -> dict:
    parts = property_string.split(',')
     
     # Extract address and determine property type and suburb
    address = parts[1]
    separated_address = address.split(' ')
    prop_type = 'apartment' if '/' in separated_address[0] else 'house'
    suburb = separated_address[-3]
    
    # Parse latitude and longitude, with validation
    latitude = float(parts[5]) if parts[5] else None
    longitude = float(parts[6]) if parts[6] else None

    if latitude and not -90 <= latitude <= 90:
        raise ValueError("Latitude must be within the range -90 to 90 degrees.")
    if longitude and not -180 <= longitude <= 180:
        raise ValueError("Longitude must be within the range -180 to 180 degrees.")

    # Construct property dictionary
    property_dict = {
        'prop_id': parts[0],
        'prop_type': prop_type,
        'full_address': address,
        'suburb': suburb,
        'bedrooms': int(parts[2]) if parts[2] else None,
        'bathrooms': int(parts[3]) if parts[3] else None,
        'parking_spaces': int(parts[4]) if parts[4] else None,
        'latitude': latitude,
        'longitude': longitude,
        'floor_number': int(parts[7]) if parts[7] else None,
        'land_area': int(parts[8]) if parts[8] else None,
        'floor_area': int(parts[9]) if parts[9] else None,
        'price': int(parts[10]) if parts[10] else None,
        'property_features': parts[11].split(';') if parts[11] else []  
    }
    return property_dict


def read_property_file(file_path: str) -> list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        next(file)  
        return [line.strip() for line in file]


def save_to_json(data: list, output_path: str) -> None:
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)


def add_feature(property_dict: dict, feature: str) -> None:
    if feature not in property_dict['property_features']:
        property_dict['property_features'].append(feature)


def remove_feature(property_dict: dict, feature: str) -> None:
    if feature in property_dict['property_features']:
        property_dict['property_features'].remove(feature)

def main():
    property_strings = read_property_file(PROPERTIES_FILE)
    processed_data = []

    for property_string in property_strings:
        try:
            property_dict = extract_information(property_string)
            processed_data.append(property_dict)
        except ValueError as e:
            print(f"Error processing property string: {property_string}. Error: {e}")

    save_to_json(processed_data, EXTRACTED_PROPERTIES)
    print(f"Processed data saved to {EXTRACTED_PROPERTIES}")


if __name__ == '__main__':
    main()