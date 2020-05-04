import pandas as pd
import matplotlib.pyplot as plt
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
# House prices data
house_prices = pd.read_csv('data/sao-paulo-properties-april-2019.csv')
house_prices.columns = house_prices.columns.str.lower().str.replace(' ', '_')

# Sao Paulo Metro Stations data
metro = pd.read_csv('data/metrosp_stations.csv', index_col='station', sep=';')

# Extracting some useful information for calculating the distances
# between the houses and the metro stations
properties_coords = list(zip(house_prices['longitude'], house_prices['latitude']))
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
    radius = 6371 # m -> change earth radius for results in other units

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
house_prices['nearest_station'] = [names for names, distance in property_distances]
house_prices['nearest_station_distance'] = [distance for names, distance in property_distances]

# From now on we'll be working only with properties for rent
# Filtering the data according to the negotiation type
rent = house_prices[house_prices['negotiation_type'] == 'rent']
# sale = house_prices[house_prices['negotiation_type'] == 'sale']

# Filtering the data according to the distance to the nearest subway station
# rent = rent[rent['nearest_station_distance'] <= 1]

# Numerical and Categorical features
# numerical = rent.dtypes[rent.dtypes != "object"].index
# categorical = rent.dtypes[rent.dtypes == "object"].index


def remove_outliers(dataframe):
    """
    Interquartile range (IQR) is a measure of statistical dispersion,
    being equal to the difference between 75th and 25th percentiles.

    This function removes outliers from the given dataframe using
    """
    Q1 = dataframe.quantile(0.25)
    Q3 = dataframe.quantile(0.75)
    IQR = Q3 - Q1
    updated = dataframe[~((dataframe < (Q1 - 1.5 * IQR)) | (dataframe > (Q3 + 1.5 * IQR))).any(axis=1)]
    return updated


rent_updated = remove_outliers(rent)

# Comparing the data before and after removing outliers with IQR technique
fig, axs = plt.subplots(1, 2)
axs[0].boxplot(rent['price'])
axs[0].set_title('With Outliers')
axs[1].boxplot(rent_updated['price'])
axs[1].set_title('Without outliers')
plt.show()

# Storing the rent data in a new csv
rent_updated.to_csv('data/rent_data.csv', index=False)

print(f"--- the script ran in {time.time() - start_time} seconds --- ")