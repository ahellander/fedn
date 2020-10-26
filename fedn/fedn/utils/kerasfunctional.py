#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : kerasfunctional.py
# Author            : Sheetal Reddy <sheetal.reddy@ai.se>
# Date              : 26.10.2020
# Last Modified Date: 26.10.2020
# Last Modified By  : Sheetal Reddy <sheetal.reddy@ai.se>
import os
import tempfile
import numpy as np
import tensorflow.keras.models as krm
import collections
from .helpers import HelperBase
from yolo3 import yolo_head, box_iou 
import tensorflow as tf

class KerasFunctionalHelper(HelperBase):
    """ FEDn helper class for keras.Sequential. """

    def average_weights(self, models):
        """ Average weights of Keras Sequential models. """
        weights = [model.get_weights() for model in models]

        avg_w = []
        for l in range(len(weights[0])):
            lay_l = np.array([w[l] for w in weights])
            weight_l_avg = np.mean(lay_l, 0)
            avg_w.append(weight_l_avg)

        return avg_w

    def increment_average(self, model, model_next, n):
        """ Update an incremental average. """
        w_prev = self.get_weights(model)
        w_next = self.get_weights(model_next)
        w = np.add(w_prev, (np.array(w_next) - np.array(w_prev)) / n)
        self.set_weights(model, w)

    def set_weights(self, model, weights):
        model.set_weights(weights)

    def get_weights(self, model):
        return model.get_weights()

    def save_model(self, model, path):
        model.save(path)

    def load_model(self, model, objects = {'yolo_head': yolo_head, 'tf':tf, 'box_iou': box_iou}):
        """ We need to go via a tmpfile to load bytestream serializd models retrieved from the miniorepository. """
        fod, outfile_name = tempfile.mkstemp(suffix='.h5')
        with open(outfile_name, 'wb') as fh:
            s = fh.write(model)
            print("Written {}".format(s),flush=True)
            fh.flush()
        fh.close()
        model = krm.load_model(outfile_name, custom_objects = objects)
        os.unlink(outfile_name)
        return model
