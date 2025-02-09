import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('seattlehouses.csv')

data

data.info()

# Some descriptive staff -> part I.
feature_stats = data.describe()

# 1.1 Visual Exploration:
data.hist(bins=20, figsize=(15, 10))

# part II.
# 1.2 Correlation with Target Variable
correlation_matrix = data.corr()
target_correlation = correlation_matrix['price'].sort_values(ascending=False)
# print(target_correlation)
import seaborn as sns
# 1.3 Pairwise Feature Relationships
sns.pairplot(data, x_vars=['size', 'beds', 'baths', 'lot_size'], y_vars='price', kind='scatter')

# we see outliers of which we're gonna rid of further

#CONVERT ACRE TO SAFT AND REMOVE UNIT FEATURES
# Conversion factor: 1 acre = 43560 sqft
acre_to_sqft_conversion = 43560

# Convert 'lot_size' to 'sqft' for rows where 'lot_size_units' is 'acre'
data.loc[data['lot_size_units'] == 'acre', 'lot_size'] *= acre_to_sqft_conversion

# Drop the 'lot_size_units' column if it's no longer needed
data.drop('lot_size_units', axis=1, inplace=True)
data.drop('size_units', axis=1, inplace=True)

data.info()

#data.dropna(inplace=True)

# Calculate the mean of the "size" column excluding null values
mean_size = data['lot_size'].mean()

# Replace null values in the "size" column with the mean
data['lot_size'].fillna(mean_size, inplace=True)
data

neural_data = data.copy()

data.drop('zip_code',axis=1,inplace=True)

data['beds_baths_interaction'] = data['beds'] * data['baths']
data['beds_squared'] = data['beds'] **2

# Extract the "price" column
price_column = data['price']

# Drop the "price" column from the DataFrame
data.drop(columns=['price'], inplace=True)

# Add the "price" column as the last column in the DataFrame
data['price'] = price_column

## Linear regression implementation
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming df is your DataFrame with the variables of interest
# Scatter plot
sns.scatterplot(x='size', y='price', data=data)

# Fit and plot the regression line
sns.regplot(x='size', y='price', data=data, scatter=False, color='red')

# Identify outliers using statistical method like z-score
#  'size' wrt 'price' have outliers

# Calculate z-scores for 'size' and 'price'
z_scores_size = (data['size'] - data['size'].mean()) / data['size'].std()
z_scores_price = (data['price'] - data['price'].mean()) / data['price'].std()

# Define a threshold for outlier detection
threshold = 5

# Color outliers differently
outlier_mask = (z_scores_size > threshold) | (z_scores_price > threshold)
sns.scatterplot(x='size', y='price', data=data[~outlier_mask], color='blue')
sns.scatterplot(x='size', y='price', data=data[outlier_mask], color='red', label='Outliers')

# Set plot labels and title
plt.xlabel('size')
plt.ylabel('price')
plt.title('Scatter plot with regression line and outliers')

# Show legend
plt.legend()

# Show plot
plt.show()

data.corr()

# Filter the DataFrame to remove outliers
data_without_outliers = data[~outlier_mask]

from sklearn.model_selection import train_test_split

x=data_without_outliers.drop(['price'], axis=1)
y= data_without_outliers['price']

x_train_temp, x_test, y_train_temp, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train_temp, y_train_temp, test_size=0.25, random_state=42)
# Print the shapes of the resulting datasets
print("Training data:", x_train.shape, y_train.shape)
print("Validation data:", x_val.shape, y_val.shape)
print("Test data:", x_test.shape, y_test.shape)

x_train, y_train = x_train.to_numpy(), y_train.to_numpy()
x_val, y_val = x_val.to_numpy(), y_val.to_numpy()
x_test, y_test = x_test.to_numpy(), y_test.to_numpy()

x_train.shape, y_train.shape, x_val.shape, y_val.shape, x_test.shape, y_test.shape

from sklearn.metrics import mean_squared_error as mse, r2_score
from sklearn.linear_model import LinearRegression

lm = LinearRegression().fit(x_train, y_train)
y_pred = lm.predict(x_val)
mse_train = mse(lm.predict(x_train), y_train, squared=False)
mse_val = mse(lm.predict(x_val), y_val, squared=False)
mse_test = mse(lm.predict(x_test), y_test, squared=False)
r_squared = r2_score(y_val, y_pred)
print("R2 ", r_squared)
print("Root MSE VAL ", mse_val)
print("Root MSE TRAIN", mse_train)

# 1 Decision Tree Algorithm
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
# Initialize Decision Tree model
dt_model = DecisionTreeRegressor(max_depth=5)

# Train the model
dt_model.fit(x_train, y_train)

# Make predictions on the test set
y_pred = dt_model.predict(x_test)


# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("R-squared:", r2)

from sklearn.metrics import explained_variance_score

# Assuming you have a trained Decision Tree model named dt_model
# and X_test, y_test as your test set

# Predictions using the Decision Tree model
y_pred = dt_model.predict(x_test)

# Calculate the explained variance score
explained_var_score = explained_variance_score(y_test, y_pred)

# Print or use the explained variance score
print("Explained Variance Score:", explained_var_score)

# Step Feature Importance:
feature_importances = dt_model.feature_importances_

# Get feature names from the original DataFrame
feature_names = x.columns

# Create a bar plot to visualize feature importance
plt.bar(range(len(feature_importances)), feature_importances)
plt.xlabel('Feature Index')
plt.ylabel('Feature Importance')
plt.xticks(range(len(feature_importances)), feature_names, rotation=45)
plt.title('Decision Tree Feature Importance')
plt.show()

# Graph
from sklearn.tree import DecisionTreeRegressor, export_graphviz
import graphviz

dot_data = export_graphviz(dt_model, out_file=None, impurity=False)
graph = graphviz.Source(dot_data)
graph

# Check overfitting
train_score = dt_model.score(x_train, y_train)
test_score = dt_model.score(x_test, y_test)

print("Training R-squared:", train_score)
print("Test R-squared:", test_score)

# Trying to visualize
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

train_sizes, train_scores, test_scores = learning_curve(dt_model, x, y, cv=5)

plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training Score')
plt.plot(train_sizes, np.mean(test_scores, axis=1), label='Test Score')
plt.xlabel('Training Set Size')
plt.ylabel('R-squared')
plt.legend()
plt.show()

# Cross validation
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(dt_model, x, y, cv=5)
print("Cross-Validation Scores:", cv_scores)

mean_cv_score = np.mean(cv_scores)
print("Mean Cross-Validation Score:", mean_cv_score)

neural_data

## Implementing the Neural Network
from sklearn.preprocessing import LabelEncoder
label_encoder_lot_set_units = LabelEncoder()
label_encoder_zip_codes = LabelEncoder()

neural_data["zip_code"] =  label_encoder_zip_codes.fit_transform(neural_data["zip_code"])

neural_data



import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error, mean_squared_error
model = Sequential()
model.add(Dense(128, input_dim = 6, kernel_initializer = 'normal', activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(64, input_dim = 6, kernel_initializer = 'normal', activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation = 'linear'))


model.add(Dense(1, activation =  'linear'))
optimizer = Adam()

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae', 'mse'])

print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

# Train the model
history =model.fit(x_train, y_train, epochs=300, batch_size=500, validation_data=(x_test, y_test), verbose=1)

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss During Training')
plt.legend()
plt.show()

test_accuracy = model.evaluate(x_test, y_test)

mse_neural = test_accuracy[2]

print(f"Test Accuracy: {test_accuracy}")
variance = np.var(y_test)
R_squared = 1 - (mse_neural/variance)
print(f"R-Squared: {R_squared}")
print(f"Mean Absolute Error:  {test_accuracy[1]}")
print(f"Mean Squared Error: {test_accuracy[2]}")

y_train_pred =model.predict(x_train)
y_test_pred = model.predict(x_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_train, y_train_pred, color='#99EDC3', alpha=0.5, label='Training Data')
plt.scatter(y_test, y_test_pred, color='#FFDAB9', alpha=0.5, label='Testing Data')

plt.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=2, label='Ideal Prediction')

plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs. Actual Values')
plt.legend()

plt.tight_layout()
plt.show()

