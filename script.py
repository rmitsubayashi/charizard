import tensorflow as tf
import numpy as np
import skimage
from skimage import data, transform
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
from google.colab import files

    
def read_parties():
    x_file_name = "normalizedPartiesX.txt"
    y_file_name = "normalizedPartiesY.txt"
    x_type_file_name = "pokemonTypesX.txt"
    y_type_file_name = "pokemonTypesY.txt"
    
    test_labels = []
    test_parties = []
    test_types = []
    training_labels = []
    training_parties = []
    training_types = []
    
    i=0
    with open(x_file_name, "r") as file, open(x_type_file_name, "r") as typeFile:
        for line in file :
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsInt = []
            typesInt = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsInt.append(id)
                typeLine = typeFile.readline()
                types = typeLine.split(",")
                typesInt = []
                typesInt.append(int(types[0]))
                if len(types) == 1 :
                    typesInt.append(0)
                else :
                    typesInt.append(int(types[1]))
                
                    
            if i%5==1 :
                test_parties.append(idsInt)
                test_types.append(typesInt)
                test_labels.append(0)
            else :
                training_parties.append(idsInt)
                training_types.append(typesInt)
                training_labels.append(0)
            i += 1
    
    
    with open(y_file_name, "r") as file, open(y_type_file_name, "r") as typeFile:
        for line in file :
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsInt = []
            typesInt = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsInt.append(id)
                typeLine = typeFile.readline()
                types = typeLine.split(",")
                typesInt = []
                typesInt.append(int(types[0]))
                if len(types) == 1 :
                    typesInt.append(0)
                else :
                    typesInt.append(int(types[1]))
            
            if i%5==1 :
                test_parties.append(idsInt)
                test_types.append(typesInt)
                test_labels.append(1)
            else :
                training_parties.append(idsInt)
                training_types.append(typesInt)
                training_labels.append(1)
            i += 1
        
    return training_parties, training_types, training_labels, test_parties, test_types, test_labels
 
def main(unused_argv):
    #normalizedParties
    print("normalizedPartiesX")
    try: 
      os.remove("normalizedPartiesX.txt")
    except OSError:
      pass
    files.upload()
    print("normalizedPartiesY")
    try:
      os.remove("normalizedPartiesY.txt")
    except OSError:
      pass
    files.upload()
    #types
    print("pokemonTypesX")
    try:
      os.remove("pokemonTypesX.txt")
    except OSError:
      pass
    files.upload()
    print("pokemonTypesY")
    try:
      os.remove("pokemonTypesY.txt")
    except OSError:
      pass
    files.upload()
    training_parties, training_types, training_labels, test_parties, test_types, test_labels = read_parties()
    training_labels = np.array(training_labels)
    test_labels = np.array(test_labels)
    training_parties = np.array(training_parties)
    test_parties = np.array(test_parties)
    test_types = np.array(test_types)
    training_types = np.array(training_types)
    
    
    ids = tf.feature_column.categorical_column_with_identity(
      'ids', 387)
    types = tf.feature_column.categorical_column_with_identity(
      'types', 19)
    feature_columns = [tf.feature_column.indicator_column(ids),
                       tf.feature_column.indicator_column(types)]
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[100,20],
        optimizer=tf.train.AdamOptimizer(1e-4),
        n_classes=2,
        dropout=0.1
    )
    
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"ids": training_parties, "types": training_types},
        y=training_labels,
        num_epochs=None,
        batch_size=50,
        shuffle=True
    )
    
    classifier.train(input_fn=train_input_fn, steps=5000)
        
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"ids":test_parties, "types": test_types},
        y=test_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)
 
if __name__ == "__main__":
    tf.app.run()