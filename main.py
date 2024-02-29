from sklearn.model_selection import train_test_split
from data import parse_data
import numpy as np
from sklearn.linear_model import LinearRegression


def get_MSE(actual, predicted):
    """Calculate the mean squared error between actual and predicted values."""
    return np.mean((actual - predicted) ** 2)

def get_r2(actual, predicted):
    """Calculate the R-squared score between actual and predicted values."""
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    return 1 - (ss_res / ss_tot)



def main():
    train, validation, test, trainY, validationY, testY = parse_data()

    features = ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']  # excluding Artery
    train = np.column_stack([train[name] for name in features])
    validation = np.column_stack([validation[name] for name in features])
    test = np.column_stack([test[name] for name in features])

    model = LinearRegression()

    model.fit(train, trainY)

    valid_predictions = model.predict(validation)

    # Evaluation: the model performance on the validation set
    mse = get_MSE(validationY, valid_predictions)
    r2 = get_r2(validationY, valid_predictions)

    print(f"Validation MSE: {mse}")
    print(f"Validation R^2: {r2}")

    test_predictions = model.predict(test)
    test_mse = get_MSE(testY, test_predictions)
    test_r2 = get_r2(testY, test_predictions)

    print(f"Test MSE: {test_mse}")
    print(f"Test R^2: {test_r2}")
    # trainX = np.array(train[:, :5])
    # trainY = np.array(train[:, 5:]).T
    # testX = test[:, :-1]
    # testY = test[:, -1]
    print(test)
    print(testY)
    # model.fit(trainX, trainY)
    # preds = model.predict(testX)
    # mse_val = np.mean((preds - testY)**2)
    # print(mse_val)

main()