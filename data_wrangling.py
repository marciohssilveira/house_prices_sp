import pandas as pd
import geopy.distance as gpd

""""
the datasets for this work were obtained from 
https://www.kaggle.com/argonalyst/sao-paulo-real-estate-sale-rent-april-2019
and
https://www.kaggle.com/thiagodsd/sao-paulo-metro
the main goal of this work is to find a apartment in SP that suits the needs of people
"""
# Importing the data:
estate = pd.read_csv('sao-paulo-properties-april-2019.csv', index_col=0)
estate.columns = estate.columns.str.lower().str.replace(' ', '_')

metro = pd.read_csv('metrosp_stations.csv', index_col='station', sep=';')

# Extracting some useful information for calculating the distances
properties_coords = list(zip(estate['longitude'], estate['latitude']))
stations_coords = list(zip(metro['lon'], metro['lat']))
station_names = list(metro.index)


def get_min_distance(properties, stations, names):
    """"
    This function uses the coordinates of the properties and of the subway stations to calculate its distances
    using a geopy function. Then it will find the closest station to each property and return its name and distance.
    """"
    properties_distances = []
    stations_names = []
    for property in properties:
        station_distances = {}
        for station, name in zip(stations, names):
            station_distances[name] = gpd.distance(property, station).km
        min_distance = min(station_distances.values())
        station_name = [key for key in station_distances if station_distances[key] == min_distance]
        properties_distances.append(min_distance)
        stations_names.append(station_name)
    return list(zip(stations_names, properties_distances))


property_distances = get_min_distance(properties_coords, stations_coords, station_names)