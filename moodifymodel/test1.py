from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import  Dense,Dropout,Activation,Flatten,BatchNormalization
from keras.layers import Conv2D,MaxPooling2D
from keras.utils.vis_utils import plot_model
from keras.optimizers import RMSprop,SGD,Adam
from keras.callbacks import ModelCheckpoint,EarlyStopping,ReduceLROnPlateau
from ann_visualizer.visualize import ann_viz;
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
num_classes = 5
img_rows,img_columns = 48,48
batch_size = 8

training_data = r'C:\Users\sheru\PycharmProjects\miniproject4\images\train'
validate_data = r'C:\Users\sheru\PycharmProjects\miniproject4\images\validation'

generate_train = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    shear_range=0.3,
    zoom_range=0.3,
    width_shift_range=0.4,
    horizontal_flip=True,
    fill_mode='nearest')

generate_validate = ImageDataGenerator(rescale=1./255)

train_generator = generate_train.flow_from_directory(
    training_data,
    color_mode='grayscale',
    target_size=(img_rows,img_columns),
    batch_size = batch_size,
    class_mode='categorical',
    shuffle=True)


validate_generator = generate_validate.flow_from_directory(
    validate_data,
    color_mode='grayscale',
    target_size=(img_rows,img_columns),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True)


model = Sequential()

#CNN

#Block-1

model.add(Conv2D(32,(3,3),padding='same',kernel_initializer='he_normal', input_shape=(img_rows,img_columns,1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(32,(3,3),padding='same',kernel_initializer='he_normal',input_shape=(img_rows,img_columns,1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))


#Block-2
model.add(Conv2D(64,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(64,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))


#Block-3
model.add(Conv2D(128,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))


#Block-4
model.add(Conv2D(256,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(256,(3,3),padding='same',kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))


#Block-5
model.add(Flatten())
model.add(Dense(64,kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))


#Block-6
model.add(Dense(64,kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))


#Block-7
model.add(Dense(num_classes,kernel_initializer='he_normal'))
model.add(Activation('softmax'))

print(model.summary())
#ann_viz(model, title="Neural Network")
plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
#C:\Program Files\Graphviz\bin
'''
check = ModelCheckpoint('Mood.h5',
                        monitor='val_loss',
                        mode='min',
                        save_best_only=True,
                        verbose=1)

stop = EarlyStopping(monitor='val_loss',
                     min_delta=0,
                     patience=3,
                     verbose=1,
                     restore_best_weights=True
                     )

reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                              factor=0.2,
                              patience=3,
                              verbose=1,
                              min_delta=0.0001)

callbacks = [stop,check,reduce_lr]

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.001),
              metrics=['accuracy'])

train_sample = 24282
validate_sample = 5937
epochs = 30

history = model.fit_generator(
    train_generator,
    steps_per_epoch=train_sample//batch_size,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=validate_generator,
    validation_steps=validate_sample//batch_size)'''