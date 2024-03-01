from sklearn.model_selection import train_test_split
from data import split_data, process_data
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path


def get_MSE(actual, predicted):
    """Calculate the mean squared error between actual and predicted values."""
    return np.mean((actual - predicted) ** 2)

def get_r2(actual, predicted):
    """Calculate the R-squared score between actual and predicted values."""
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    return 1 - (ss_res / ss_tot)



def main():
    folder_path = Path('data/waves')
    header = [('Artery', int), ('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]

    # Assume process_data and split_data functions are defined elsewhere in your script
    aggregated_data, aggregated_labels = process_data(folder_path, header)
    train_data, train_labels, valid_data, valid_labels, test_data, test_labels = split_data(aggregated_data, aggregated_labels)

    # Extract the features for training, validation, and testing
    features = ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']
    train_features = np.column_stack([train_data[name] for name in features])
    validation_features = np.column_stack([valid_data[name] for name in features])
    test_features = np.column_stack([test_data[name] for name in features])

    model = LinearRegression()
    model.fit(train_features, train_labels)

    # Making predictions and evaluating the model
    valid_predictions = model.predict(validation_features)
    mse = get_MSE(valid_labels, valid_predictions)
    r2 = get_r2(valid_labels, valid_predictions)

    print(f"Validation MSE: {mse}")
    print(f"Validation R^2: {r2}")

    test_predictions = model.predict(test_features)
    test_mse = get_MSE(test_labels, test_predictions)
    test_r2 = get_r2(test_labels, test_predictions)

    print(f"Test MSE: {test_mse}")
    print(f"Test R^2: {test_r2}")

    # For debugging
    print(test_features)
    print(test_labels)
    # model.fit(trainX, trainY)
    # preds = model.predict(testX)
    # mse_val = np.mean((preds - testY)**2)
    # print(mse_val)

main()