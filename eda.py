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
# sns.boxplot(rent['price'])
# plt.show()

# Broad view of data
rent.describe()

rent['price'].hist()

# Skewness and Kurtosis
skewness = rent['price'].skew()
kurtosis = rent['price'].kurt()
print(rent['price'].describe())
print(f'Skewness: {skewness}')
print(f'Kurtosis: {kurtosis}')

# Interquartile range (IQR) is a measure of statistical dispersion,
# being equal to the difference between 75th and 25th percentiles
Q1 = rent.quantile(0.25)
Q3 = rent.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

# What is this line doing?
rent_updated = rent[~((rent < (Q1 - 1.5 * IQR)) | (rent > (Q3 + 1.5 * IQR))).any(axis=1)]

rent_updated.describe()

# Distributions of data
sns.boxplot(rent_updated['price'])
plt.show()