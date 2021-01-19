#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : train.py
# Author            : Sheetal Reddy <sheetal.reddy@ai.se>
# Date              : 22.12.2020
# Last Modified Date: 22.12.2020
# Last Modified By  : Sheetal Reddy <sheetal.reddy@ai.se>
from __future__ import print_function
import sys
import tensorflow as tf
import tensorflow.keras as keras 
import tensorflow.keras.models as krm

import pickle
import yaml
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from read_data import read_data
import os   


def train(model,data,settings):
    print("-- RUNNING TRAINING --", flush=True)

    # We are caching the partition in the container home dir so that
    # the same training subset is used for each iteration for a client. 
    try:
        with open('/app/mnist_train/x.pyb','rb') as fh:
            x_train=pickle.loads(fh.read())
        with open('/app/mnist_train/y.pyb','rb') as fh:
            y_train=pickle.loads(fh.read())
        with open('/app/mnist_train/classes.pyb','rb') as fh:
            classes=pickle.loads(fh.read())
    except:
        (x_train, y_train, classes) = read_data(data,nr_examples=settings['training_samples'])

        try:
            os.mkdir('/app/mnist_train')
            with open('/app/mnist_train/x.pyb','wb') as fh:
                fh.write(pickle.dumps(x_train))
            with open('/app/mnist_train/y.pyb','wb') as fh:
                fh.write(pickle.dumps(y_train))
            with open('/app/mnist_train/classes.pyb','wb') as fh:
                fh.write(pickle.dumps(classes))
        except:
            pass

    model.fit(x_train, y_train, batch_size=settings['batch_size'], epochs=settings['epochs'], verbose=1)



    print("-- TRAINING COMPLETED --", flush=True)
    return model

if __name__ == '__main__':


    with open('settings.yaml', 'r') as fh:
        try:
            settings = dict(yaml.safe_load(fh))
        except yaml.YAMLError as e:
            raise(e)

    from fedn.utils.kerasweights import KerasWeightsHelper

    helper = KerasWeightsHelper()
    weights = helper.load_model(sys.argv[1])
    from init_model import create_seed_model
    model = create_seed_model()
    model.set_weights(weights)
    model = train(model,'../data/train.csv',settings)
    helper.save_model(model.get_weights(),sys.argv[2])

