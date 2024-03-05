import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from pathlib import Path
from data import split_data, process_data  

def evaluate_rnn_model(model, train_features, train_labels, test_features, test_labels):
    model.compile(optimizer='adam', loss='mse')
    model.fit(train_features, train_labels, epochs=10, verbose=1)
    test_loss = model.evaluate(test_features, test_labels, verbose=1)
    print(f'Test MSE: {test_loss}')

def segment_sequences(data, sequence_length):
    segments = []
    for start_idx in range(len(data) - sequence_length + 1):
        end_idx = start_idx + sequence_length
        segment = data[start_idx:end_idx]
        segments.append(segment)
    return np.array(segments)

def main():
    folder_path = Path('data/waves')
    header = [('Artery', int), ('hAbp', float), ('hIcp', float), ('Hct', float), ('ABP', float), ('CBFV', float)]
    
    aggregated_data, aggregated_labels = process_data(folder_path, header)

    sequence_length = 100  # Adjust based on your domain knowledge

    # Assuming aggregated_data is a dictionary with keys like 'hAbp', 'hIcp', etc.
    features_stacked = np.stack([segment_sequences(aggregated_data[name], sequence_length) for name in ['hAbp', 'hIcp', 'Hct', 'ABP', 'CBFV']], axis=-1)
    
    # Adjust labels accordingly. You might need to reshape or truncate your labels to match the sequences.
    # For instance, you may take the label corresponding to the last timestep of each sequence.
    adjusted_labels = aggregated_labels[sequence_length - 1:]

    # Split data here after adjusting your labels to match the segmented sequences
    train_features, train_labels, test_features, test_labels = split_data(features_stacked, adjusted_labels)

    # Define the RNN model
    model = Sequential([
        SimpleRNN(50, activation='relu', input_shape=(sequence_length, train_features.shape[2])),
        Dense(1)
    ])

    evaluate_rnn_model(model, train_features, train_labels, test_features, test_labels)

if __name__ == "__main__":
    main()
