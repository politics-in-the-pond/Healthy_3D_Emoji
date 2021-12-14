import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2 as cv
import os

def readIndex(directory):
    if not os.path.exists(directory):
        return 0
    else:
        with open(directory, "r") as file:
            indexstr = file.readline()
            return int(indexstr)

def main() :
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in tf.config.experimental.list_physical_devices("GPU"):
                tf.config.experimental.set_virtual_device_configuration(
                    gpu,
                    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    PATH = os.path.join(os.path.expanduser('~'),'Desktop') + "\\posenet_data"

    df = pd.read_csv(PATH + '\\posenet.csv')
    labels = df['label']
    labels = labels.replace('pass', 1)
    labels = labels.replace('fail', 0)

    tf_size = 200
    #tmpimg = (np.float32(cv.resize(cv.imread(PATH+'\\images\\'+ str(1) + '.png', 1), dsize = (tf_size, tf_size), interpolation = cv.INTER_NEAREST)) - 127.5) / 127.5
    #print(tmpimg.shape)
    index = readIndex(PATH + "\\index.txt")
    
    Xtmp = []
    Y = labels.to_numpy()

    for i in range(0, index) :
        Xtmp.append( (np.float32(cv.resize(cv.imread(PATH+'\\images\\'+ str(i+1) + '.png', 1), dsize = (tf_size, tf_size), interpolation = cv.INTER_NEAREST)) - 127.5) / 127.5 )
        if (i % 500) == 0 :
            print(i)
    X = np.array(Xtmp)
    del Xtmp

    #split train dataset and test dataset
    X_1, X_test, Y_1, Y_test = train_test_split(X,Y, test_size=0.3)
    X_train, X_val, Y_train, Y_val = train_test_split(X_1,Y_1, test_size=0.15)
    print(index)

    del X
    del X_1
    del Y_1

    print(X_train.shape)

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(input_shape=(tf_size,tf_size,3), kernel_size=(3,3), filters=32, padding='same'),
        tf.keras.layers.MaxPool2D(strides=(2,2), padding='same'),
        tf.keras.layers.Conv2D(kernel_size=(3,3), filters=64, padding='same'),
        tf.keras.layers.MaxPool2D(strides=(2,2), padding='same'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=128, activation='relu'),
        tf.keras.layers.Dropout(rate=0.3),
        tf.keras.layers.Dense(units=2, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, Y_train, batch_size=32, epochs=8, validation_data=(X_val, Y_val))

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], 'b-', label='loss')
    plt.plot(history.history['val_loss'], 'r--', label='val_loss')
    plt.xlabel('Epoch')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], 'g-', label='accuracy')
    plt.plot(history.history['val_accuracy'], 'k--', label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylim(0.7, 1)
    plt.legend()

    plt.show()

    model.evaluate(X_test, Y_test, verbose=0)

    model.save(PATH + '\\model.h5')

main()
