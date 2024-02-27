from sklearn.model_selection import train_test_split
from data import parse_data
import numpy as np
from sklearn.linear_model import LinearRegression



def main():
    train, validation, test, trainY, validationY, testY = parse_data()
    
    # model = LinearRegression()
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