# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:18:32 2018

@author: sogi
"""

import tensorflow as tf
hello = tf.constant('Hello, Tensorflow')
sess = tf.Session()
print(sess.run(hello))