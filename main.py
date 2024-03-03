from sklearn.model_selection import train_test_split
from data import split_data, process_data
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path

def get_MSE(actual, predicted):
    """Calculate the mean squared error between actual and predicted values."""
    return np.mean((actual - predicted) ** 2)

def get_r2(actual, predicted):
    """Calculate the R-squared score between actual and predicted values."""
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    return 1 - (ss_res / ss_tot)

import time

def evaluate_model(model, train_features, train_labels, validation_features, valid_labels, test_features, test_labels):
    print(f"Training {model.__class__.__name__}...")
    start_time = time.time()
    model.fit(train_features, train_labels)
    print(f"Trained {model.__class__.__name__} in {time.time() - start_time:.2f} seconds.")
    
    print(f"Predicting with {model.__class__.__name__}...")
    start_time = time.time()
    valid_predictions = model.predict(validation_features)
    test_predictions = model.predict(test_features)
    print(f"Predicted with {model.__class__.__name__} in {time.time() - start_time:.2f} seconds.")

    print(f"Model: {model.__class__.__name__}")
    print(f"Validation MSE: {get_MSE(valid_labels, valid_predictions)}")
    print(f"Validation R^2: {get_r2(valid_labels, valid_predictions)}")
    print(f"Test MSE: {get_MSE(test_labels, test_predictions)}")
    print(f"Test R^2: {get_r2(test_labels, test_predictions)}")
    print("\n")


def main():
    folder_path = Path('data/waves')
    header = [('Artery', int), ('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]

    aggregated_data, aggregated_labels = process_data(folder_path, header)
    train_data, train_labels, valid_data, valid_labels, test_data, test_labels = split_data(aggregated_data, aggregated_labels)

    features = ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']
    train_features = np.column_stack([train_data[name] for name in features])
    validation_features = np.column_stack([valid_data[name] for name in features])
    test_features = np.column_stack([test_data[name] for name in features])

    linear_model = LinearRegression()
    ridge_model = Ridge()
    rf_model = RandomForestRegressor(n_estimators=10, max_depth=10, verbose=2, n_jobs=-1)


    for model in [linear_model, ridge_model, rf_model]:
        evaluate_model(model, train_features, train_labels, validation_features, valid_labels, test_features, test_labels)
    
    # For debugging
    print(test_features)
    print(test_labels)
    # model.fit(trainX, trainY)
    # preds = model.predict(testX)
    # mse_val = np.mean((preds - testY)**2)
    # print(mse_val)
main()
