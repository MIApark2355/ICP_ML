import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from pathlib import Path
from data import split_data, process_data  # Assuming these functions are defined in your 'data' module

def evaluate_rnn_model(model, train_features, train_labels, test_features, test_labels):
    model.compile(optimizer='adam', loss='mse')
    model.fit(train_features, train_labels, epochs=10, verbose=1)
    
    test_loss = model.evaluate(test_features, test_labels, verbose=1)
    print(f'Test MSE: {test_loss}')

def main():
    folder_path = Path('data/waves')
    header = [('Artery', int), ('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]

    aggregated_data, aggregated_labels = process_data(folder_path, header)
    train_data, train_labels, valid_data, valid_labels, test_data, test_labels = split_data(aggregated_data, aggregated_labels)

    # Assuming your features are in the correct shape for RNN [samples, timesteps, features]
    train_features = np.array([train_data[name] for name in ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']]).transpose((1, 0, 2))
    test_features = np.array([test_data[name] for name in ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']]).transpose((1, 0, 2))

    # Define the RNN model
    model = Sequential([
        SimpleRNN(50, activation='relu', input_shape=(train_features.shape[1], train_features.shape[2])),
        Dense(1)
    ])

    evaluate_rnn_model(model, train_features, train_labels, test_features, test_labels)

if __name__ == "__main__":
    main()