import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import pickle
import time
start_time = time.time()

# Open csv
data = pd.read_csv('rent_data.csv')

# Feature engineering
data['total_price'] = data['price'] + data['condo']

# Extract X and y
X = data[['size', 'rooms', 'toilets', 'suites', 'parking', 'nearest_station_distance']]
y = data['total_price'].values.reshape(-1, 1)

print(f'Feature extraction finished in: {time.time() - start_time} seconds')

# Separate into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)


# ===========Build model============
pipeline = Pipeline([('normalize', MinMaxScaler()), ('model', KNeighborsRegressor())])
knn_regressor = pipeline.fit(X_train, y_train)

print(f'Model training finished in: {time.time() - start_time} seconds\n')

y_pred = knn_regressor.predict(X_test)

# Metrics
print('Metrics:')
print(f'MSE: {mean_squared_error(y_test, y_pred)}')
print(f'MAE: {mean_absolute_error(y_test, y_pred)}')
print(f'R2 Score: {r2_score(y_test, y_pred)}')

# Exporting a binary
with open('real_estate_regression.pickle', 'wb') as file:
    pickle.dump(knn_regressor, file)

with open('real_estate_regression.pickle', 'rb') as file:
    my_model = pickle.load(file)

print('\nTesting with some data:')

# Testing with my own data
my_input = {'size': 60, 'rooms': 1, 'toilets': 1, 'suites': 0, 'parking': 0, 'nearest_station_distance': 0.5}
my_input_adjusted = pd.DataFrame([my_input])
my_prediction = my_model.predict(my_input_adjusted)
print(f'>Based on: {my_input}\n>>The predicted value for the property is: R${my_prediction[0][0]:.2f}')


print(f'\n\nAll finished in: {time.time() - start_time} seconds')
