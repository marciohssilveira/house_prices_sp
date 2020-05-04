import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reading the CSV and storing its contents into a Data Frame
estate = pd.read_csv('real_estate_sp.csv', index_col=False)

# Filtering the data according to the negotiation type
rent = estate[estate['negotiation_type'] == 'rent']
# sale = estate[estate['negotiation_type'] == 'sale']

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
rent_updated.to_csv('rent_data.csv', index=False)