import tensorflow as tf
import numpy as np
import skimage
from skimage import data, transform
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os

def cnn_model_fn(features, labels, mode):
    input_layer = tf.reshape(features["x"],[-1, 5, 1])
    conv1 = tf.layers.conv1d(
        inputs=input_layer,
        filters=5,
        kernel_size=5,
        padding="same",
        activation=tf.nn.relu)
        
    pool1 = tf.layers.max_pooling1d(
        inputs=conv1,
        pool_size=2,
        strides=2)
        
    #kernel size = [5,5]
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=25,
        kernel_size=5,
        padding="same",
        activation=tf.nn.relu)
        
    pool2 = tf.layers.max_pooling1d(
        inputs=conv2,
        pool_size=2,
        strides=2)
        
    dense = tf.layers.dense(
        inputs=pool2_flat, 
        units=1024,
        activation=tf.nn.relu)
    dropout = tf.layers.dropout(
        inputs=dense,
        rate=0.4,
        training=mode == tf.estimator.ModeKeys.TRAIN)
        
    logits = tf.layers.dense(
        inputs=dropout,
        units=10)
        
    predictions = {
        "classes": tf.argmax(input=logits, axis=1),
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }
    
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode-mode, predictions=predictions)
    
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
    
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels,
            predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        eval_metric_ops=eval_metric_ops)

    
def read_parties():
    ROOT_PATH = "C://Users/ryomi/Desktop/machine_learning/pattern_recognition/charizard"   
    x_file_name = ROOT_PATH + "/formattedPartiesX.txt"
    y_file_name = ROOT_PATH + "/formattedPartiesY.txt"
    
    test_labels = []
    test_parties = []
    training_labels = []
    training_parties = []
    
    i=0
    with open(x_file_name, "r") as file:
        for line in file :
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsFloat = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsFloat.append(idStr)
                    
            if i%5==0 :
                test_parties.append(idsFloat)
                test_labels.append(0)
            else :
                training_parties.append(idsFloat)
                training_labels.append(0)
            i += 1
    
    with open(y_file_name, "r") as file:
        for line in file :
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsFloat = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsFloat.append(idStr)
                    
            if i%5==0 :
                test_parties.append(idsFloat)
                test_labels.append(1)
            else :
                training_parties.append(idsFloat)
                training_labels.append(1)
            i += 1
        
    print(str(i))
    return training_parties, training_labels, test_parties, test_labels
 
def main(unused_argv):
    training_parties, training_labels, test_parties, test_labels = read_parties()
    training_labels = np.array(training_labels)
    test_labels = np.array(test_labels)
    training_parties = np.array(training_parties)
    test_parties = np.array(test_parties)
    
    feature_columns = [tf.feature_column.numeric_column("x", shape=[5])]
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[368,20,20],
        optimizer=tf.train.AdamOptimizer(1e-4),
        n_classes=2,
        dropout=0.1,
        model_dir="./tmp/charizard_model"
    )
    
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": training_parties},
        y=training_labels,
        num_epochs=None,
        batch_size=50,
        shuffle=True
    )
    
    classifier.train(input_fn=train_input_fn, steps=100000)
        
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x":test_parties},
        y=test_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)
 
if __name__ == "__main__":
    tf.app.run()