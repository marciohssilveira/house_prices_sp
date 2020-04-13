import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# supressing scientific notation on this notebook and using two decimals
pd.options.display.float_format = '{:.2f}'.format

# Reading the CSV and storing its contents into a Data Frame
rent = pd.read_csv('rent_properties.csv', index_col=False)

# Filtering the data according to the distance to the nearest subway station
# estate = estate[estate['nearest_station_distance'] <= 1]

# Numerical and Categorical features
# numerical = rent.dtypes[rent.dtypes != "object"].index
# categorical = rent.dtypes[rent.dtypes == "object"].index

# Setting styles and colours for the graphics
sns.set_style('darkgrid')
sns.set_palette('pastel')

# Distributions of data
sns.boxplot(rent['price'])
plt.show()

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

# Distributions of data
sns.boxplot(rent_updated['price'])
plt.show()