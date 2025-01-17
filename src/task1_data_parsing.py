"""
Task 1: Data Extraction and Transformation 

Background:
Real estate agencies and analysts often receive raw, unstructured property data from external sources.
This data, while valuable, is not immediately usable for analysis or decision-making. For example, details 
such as property type, location, features and pricing may be incomplete or inconsistent.

Purpose:
This script focuses on transforming raw property data strings into a clean, structured format.
The extracted data includes essential details such as:
- Property ID, type and address.
- Geolocation (latitude, longitude).
- Features like bedrooms, bathrooms, parking spaces and more.

Additionally, it provides utility functions to dynamically update the features of a property.

Key Features:
1. Parses raw property strings in CSV format and extracts key details into a dictionary.
2. Handles missing or incomplete data gracefully.
3. Validates geolocation data (latitude and longitude).
4. Includes utility functions to add or remove features from a property's feature list.
5. Outputs a structured JSON file for downstream processes (to be implemented).

Inputs:
- Raw property strings from a file (e.g., 'data/raw/property_strings.txt').

Outputs:
- Processed property data saved as a JSON file (e.g., 'data/processed/cleaned_properties.json').

Usage:
1. Place the raw property data in the input file ('data/raw/property_strings.txt').
2. Run this script to process the data:
   $ python src/task1_data_parsing.py
3. The cleaned data will be saved in 'data/processed/cleaned_properties.json'.

Functions:
1. `extract_information(property_string: str) -> dict`:
   - Extracts key details from a raw property string and returns a structured dictionary.

2. `add_feature(property_dict: dict, feature: str) -> None`:
   - Adds a specified feature to the property's feature list, if it doesn't already exist.

3. `remove_feature(property_dict: dict, feature: str) -> None`:
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
"""

import json
import os

def extract_information(property_string: str) -> dict:
    """Extracts information from the property string and creates a dictionary for the property."""
    # Split the CSV string into a list of values
    parts = property_string.split(',')

    # Extracting address from the property string
    address = parts[1]

    # Separate address string and determine property type and suburb
    separated_address = address.split(' ')
    prop_type = 'apartment' if '/' in separated_address[0] else 'house'
    suburb = separated_address[-3]

    # Initialize latitude and longitude as None
    latitude = None
    longitude = None

    # Validate and parse latitude
    if parts[5]:
        latitude = float(parts[5])
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be within the range -90 to 90 degrees.")

    # Validate and parse longitude
    if parts[6]:
        longitude = float(parts[6])
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be within the range -180 to 180 degrees.")

    # Create the dictionary with the derived information
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
        'property_features': parts[11].split(';') if parts[11] else []  # Split features by semicolon
    }

    return property_dict


def read_property_file(file_path: str) -> list:
    """Reads property data from a file and returns a list of property strings."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def save_to_json(data: list, output_path: str) -> None:
    """Saves the list of property dictionaries to a JSON file."""
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)


def add_feature(property_dict: dict, feature: str) -> None:
    """Adds a feature to the property features list."""
    if feature not in property_dict['property_features']:
        property_dict['property_features'].append(feature)


def remove_feature(property_dict: dict, feature: str) -> None:
    """Removes a feature from the property features list."""
    if feature in property_dict['property_features']:
        property_dict['property_features'].remove(feature)


def main():
    # Input and output file paths
    input_file = 'data/raw/property_strings.txt'
    output_file = 'data/processed/cleaned_properties.json'

    # Read property strings from the file
    property_strings = read_property_file(input_file)

    # Processed data list
    processed_data = []

    for property_string in property_strings:
        try:
            property_dict = extract_information(property_string)
            processed_data.append(property_dict)
        except ValueError as e:
            print(f"Error processing property string: {property_string}. Error: {e}")

    # Save the processed data to a JSON file
    save_to_json(processed_data, output_file)
    print(f"Processed data saved to {output_file}")

    # Additional feature management examples
    if processed_data:
        add_feature(processed_data[0], 'electric hot water')
        print(f"Updated features for property {processed_data[0]['prop_id']}: {processed_data[0]['property_features']}")

        remove_feature(processed_data[1], 'balcony')
        print(f"Updated features for property {processed_data[1]['prop_id']}: {processed_data[1]['property_features']}")


if __name__ == '__main__':
    main()
