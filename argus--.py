
banner = """argus
A simple OSINT tool for geolocation and mapping.
Usage:
    python argus.py "New York, USA" "Eiffel Tower, Paris" 
    This will geolocate the provided queries and create an interactive map with markers for each location.
    Requirements:
    - Python 3.x
    - geopy
    - folium
    - requests
    - beautifulsoup4
    Install dependencies:
    pip install geopy folium requests beautifulsoup4
    """

import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
import folium

from geopy.geocoders import Nominatim
import webbrowser
def geolocate(query):
    geolocator = Nominatim(user_agent="argus_geolocator")
    location = geolocator.geocode(query)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None
def create_map(locations):
    if not locations:
        print("No valid locations found.")
        return None
    avg_lat = sum(loc[0] for loc in locations) / len(locations)
    avg_lon = sum(loc[1] for loc in locations) / len(locations)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=2)
    for lat, lon in locations:
        folium.Marker([lat, lon]).add_to(m)
    return m
def main():
    parser = argparse.ArgumentParser(description="Argus - OSINT Geolocation Tool")
    parser.add_argument("queries", nargs="+", help="Location queries to geolocate")
    args = parser.parse_args()
    locations = []
    for query in args.queries:
        loc = geolocate(query)
        if loc:
            print(f"Geolocated '{query}' to {loc}")
            locations.append(loc)
        else:
            print(f"Could not geolocate '{query}'")
    map_obj = create_map(locations)
    if map_obj:
        map_file = "argus_map.html"
        map_obj.save(map_file)
        print(f"Map saved to {map_file}")
        webbrowser.open(map_file)

if __name__ == "__main__":
    main()
