#! /usr/bin/python3
# coding:utf-8

#pip install graphic-verification-code

import random,os
import numpy as np
import tensorflow as tf


number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

IMAGE_HEIGHT = 25
IMAGE_WIDTH = 80
CHAR_SET = number + ALPHABET
CAPTCHA_SIZE = 4

def captcha_cnn():
    input_tensor = tf.keras.Input(shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))

    x = input_tensor
    for i, n in enumerate([2,2,2]):
        for _ in range(n):
            x = tf.keras.layers.Conv2D(16*2**min(i, 3), kernel_size=3, padding='same', activation='relu', kernel_initializer='he_uniform')(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.MaxPool2D((2, 2), strides=2)(x)
        x = tf.keras.layers.Dropout(0.2)(x) if i == 0 or i == 2 else x

    x = tf.keras.layers.Flatten()(x)
    output_tensor = [tf.keras.layers.Dense(len(CHAR_SET), activation='softmax', name='c%d'%(i+1))(x) for i in range(CAPTCHA_SIZE)]

    model = tf.keras.Model(input_tensor, output_tensor)

    model.summary()

    return model

class batchpic(object):
    def __init__(self, char_set, batch_size, captcha_size):
        self.char_set = ''.join(char_set)
        self.batch_size = batch_size
        self.captcha_size = captcha_size

    def getpatches(self):
        batch_x = np.zeros((self.batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, 3))
        batch_y = [np.zeros((self.batch_size, len(self.char_set)), dtype=np.uint8) for i in range(self.captcha_size)]

        IMAGE_PATH = './pictemp/'
        images = os.listdir(IMAGE_PATH)

        for i,image in enumerate(images):
            if i == self.batch_size :
                break
            picpath = os.path.join(IMAGE_PATH,image)

            x = tf.io.read_file(picpath)        
            x = tf.image.decode_png(x, channels=3)
            x = tf.image.convert_image_dtype(x, tf.float64)             
            x /= 255.
            x = tf.reshape(x, (IMAGE_HEIGHT, IMAGE_WIDTH, 3))

            batch_x[i, :] = x
            (filename,_) = os.path.splitext(image)
            for j, ch in enumerate(filename):
                batch_y[j][i, :] = 0
                batch_y[j][i, self.char_set.index(ch)] = 1

        return batch_x, batch_y

    def vec2text(self, vec):
        text = []
        for item in vec:
            index = item[0]
            text.append(self.char_set[index])
        return ''.join(text)

class TrainAndPredict(object):
    def __init__(self, modelpath, batch_size, charset, captcha_size, epochs):
        self.model = captcha_cnn()
        self.modelpath = modelpath
        try:
            self.model.load_weights(self.modelpath + 'captcha_cnn_best.h5')
            self.model.compile(optimizer=tf.keras.optimizers.Adam(1e-4, amsgrad=True),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])
        except Exception as identifier:
            print(identifier)
            self.model.compile(optimizer=tf.keras.optimizers.Adam(1e-3, amsgrad=True),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

        self.callbacks = [tf.keras.callbacks.EarlyStopping(patience=3),
                            tf.keras.callbacks.CSVLogger(self.modelpath + 'log/captcha_cnn.csv', append=True), 
                            tf.keras.callbacks.ModelCheckpoint(self.modelpath + 'captcha_cnn_best.h5', save_best_only=True)]
        
        self.batch_size = batch_size
        self.charset = charset
        self.captcha_size = captcha_size
        self.epochs = epochs

    def train(self):

        train_data = batchpic(self.charset, self.batch_size, self.captcha_size)
        validation_data = batchpic(self.charset, 100, self.captcha_size)

        train_images, train_labels = train_data.getpatches()
        test_images, test_labels = validation_data.getpatches()

        self.model.fit(train_images, train_labels, epochs=self.epochs, 
                        validation_data=(test_images, test_labels), workers=4, use_multiprocessing=True,
                        callbacks=self.callbacks)

    def predict(self):

        test_data = batchpic(self.charset, 1, self.captcha_size)

        data_x, data_y = test_data.getpatches()
        prediction_value = self.model.predict(data_x)

        data_y = test_data.vec2text(np.argmax(data_y, axis=2))
        prediction_value = test_data.vec2text(np.argmax(prediction_value, axis=2))
        if data_y.upper() == prediction_value.upper():
            print('测试数据：', data_y, '预测数据：', prediction_value, '准确')
        else:
            print('测试数据：', data_y, '预测数据：', prediction_value, '失败')


if __name__ == '__main__':
    #MODEL_PATH = "/content/drive/APP/keras_cnn/"
    MODEL_PATH = './keras_cnn/'

    BATCH_SIZE = 999
    EPOCHS = 1

    cacnn = TrainAndPredict(MODEL_PATH, BATCH_SIZE, CHAR_SET, CAPTCHA_SIZE, EPOCHS)
    cacnn.train()
    cacnn.train()

    cacnn.predict()
