import numpy as np
import tensorflow as tf
import pickle
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/data", one_hot=True)

n_nodes_h1 = 100
n_nodes_h2 = 100
n_nodes_h3 = 100
n_classes = 10
batch_size = 100
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def model_network(data):
    hidden_layer_1 = {'weights': tf.Variable(tf.random_normal([784, n_nodes_h1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_h1]))}

    hidden_layer_2 = {'weights': tf.Variable(tf.random_normal([n_nodes_h1, n_nodes_h2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_h2]))}

    hidden_layer_3 = {'weights': tf.Variable(tf.random_normal([n_nodes_h2, n_nodes_h3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_h3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_h3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}


    l1 = tf.add(tf.matmul(data, hidden_layer_1['weights']), hidden_layer_1['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_layer_2['weights']), hidden_layer_2['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_layer_3['weights']), hidden_layer_3['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']
    
    return output


def train_neural_network(x):
    #prediction = neural_network_model(x)
    prediction = model_network(x)

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    hm_epoch = 25
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        
        for epoch in range(hm_epoch):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
            print("Epoch ", epoch, ' loss ', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1)) 

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        print('Accuracy ', accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)