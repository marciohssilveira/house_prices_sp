import pandas as pd
import math
import time
start_time = time.time()


""""
the datasets for this work were obtained from 
https://www.kaggle.com/argonalyst/sao-paulo-real-estate-sale-rent-april-2019
and
https://www.kaggle.com/thiagodsd/sao-paulo-metro
the main goal of this work is to find a apartment in SP that suits the needs of people
"""
# Importing the data:
estate = pd.read_csv('sao-paulo-properties-april-2019.csv')
estate.columns = estate.columns.str.lower().str.replace(' ', '_')

metro = pd.read_csv('metrosp_stations.csv', index_col='station', sep=';')

# Extracting some useful information for calculating the distances
properties_coords = list(zip(estate['longitude'], estate['latitude']))
stations_coords = list(zip(metro['lon'], metro['lat']))
station_names = list(metro.index)


def calculate_distance(origin, destination):
    """"
    Function to calculate a distance between two coordinates (lat, lon)
    It was made using the Haversine formula
    The results are in kilometers
    """""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km -> change earth radius for results in other units

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def get_min_distance(properties, stations, names):
    """"
    This function uses the coordinates of the properties and of the subway stations to calculate its distances
    using a geopy function. Then it will find the closest station to each property and return its name and distance.
    """""
    result = []
    for property in properties:
        min_dist = float('inf')
        min_station_name = None
        for station, name in zip(stations, names):
            dist = calculate_distance(property, station)
            if dist <= min_dist:
                min_dist = dist
                min_station_name = name

        result.append((min_station_name, min_dist))
    return result


property_distances = get_min_distance(properties_coords, stations_coords, station_names)


# Unpacking the result of the function and inserting them as new columns into the estate dataframe.
estate['nearest_station'] = [names for names, distance in property_distances]
estate['nearest_station_distance'] = [distance for names, distance in property_distances]

# Saving the new data into the csv file
estate.to_csv('real_estate_sp.csv')

print(f"--- the script ran in {time.time() - start_time} seconds --- ")