# Acknowledgement
  
This project is supported by [Segmind](https://segmind.com)

# keras JukeBox

This is a UI based hyper-parameter controller, which let's you control the following.

* start, pause and stop a live training.
* reset the learning rate on dynamically while training is in progress.
* take a snapshot at will

more functionalities are to be added

# Dependencies

This package depends on **MQTT** protocol for communication. So, it is expected that an MQTT broker is up and running in 'localhost' at port 1883(default port).

Install it by :

```

sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

```

Python dependencies:

* python >= 3.6.8
* paho-mqtt
* PyQt5
* tensorflow >= 1.14

**Note: This package is intended and tested for tensorflow-keras api and NOT keras with tensorflow 'backend'**

# Usage

you can try the following example

save the follwing example **fashion_mnist_jukebox.py**

```
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from tensorflow import keras


# import the callback
from keras_jukebox import JukeBoxCallback


fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


train_images = train_images / 255.0

test_images = test_images / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# pass the jukebox callback to model.fit method
model.fit(train_images, train_labels, epochs=10, callbacks=[JukeBoxCallback(verbose=1)])
```

and run it.
You will notice that the script starts but training doesn't, which is because it is paused and needs a JukeBox-UI to start.

Now, open a new terminal(Alt+ctrl+T) and start the JukeBox by typing:

```

start_jukebox

```

and you should see the UI pop up, note the algorithm is in **pause** mode by default. Hit the play button to start the training.