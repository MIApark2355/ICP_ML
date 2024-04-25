import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Sample data preparation
data = {
    'meanABP': [80, 85, 78, 90, 95],
    'meanCPP': [70, 75, 65, 80, 85],
    'meanICP': [20, 22, 21, 23, 25]
}
df = pd.DataFrame(data)

# Features and target
X = df[['meanABP', 'meanCPP']]
y = df['meanICP']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict the target on the training and test data
y_train_pred = model.coef_

# Predicting on test data
y_pred = model.predict(X_test)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Model coefficients
print("Model coefficients:", model.coef_)
print("Model intercept:", model.intercept_)
