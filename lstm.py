from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import matplotlib.pyplot as plt
from keras.optimizers import Adam

data_dim = 5
timesteps = 3600
MODEL_NAME = 'model_history/model1.h5'
MODEL_WEIGHTS = 'model_history/model1weights.h5'
PLOT = 'model_history/model1.png'

new_data = np.loadtxt('x_train.txt')
x_train = new_data.reshape((800, 3600, 5))
new_data = np.loadtxt('x_test.txt')
x_val = new_data.reshape((200, 3600, 5))

y_train = np.loadtxt('y_train.txt')
y_val = np.loadtxt('y_test.txt')

def plot_lstm(hist):
    # LSTM plotting
    plt.figure(figsize=(13, 8))
    plt.plot(hist.history['loss'], color='blue')
    plt.plot(hist.history['val_loss'], color='orange')
    plt.plot(hist.history['acc'], color='red')
    plt.plot(hist.history['val_acc'], color='green')
    plt.title('Training Loss and Accuracy')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['loss', 'val_loss', 'acc', ' val_acc'], loc='best')
    plt.savefig(PLOT)
    plt.show()

model = Sequential()
model.add(LSTM(32, return_sequences=True, input_shape=(timesteps, data_dim)))
# model.add(LSTM(32, return_sequences=True))
model.add(LSTM(32))
model.add(Dense(2, activation='sigmoid'))

# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(Adam(lr=0.001), loss='binary_crossentropy', metrics=['acc'])
# model.summary()
out = model.fit(x_train, y_train, batch_size=100, epochs=1, validation_data=(x_val, y_val))
model.save(MODEL_NAME)
model.save_weights(MODEL_WEIGHTS)
plot_lstm(out)
