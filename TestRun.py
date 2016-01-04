import NeuralNetwork as nn
import numpy as np
import random
import matplotlib.pyplot as plt
import math

# This file is used for testing the neural network

def crossValidate(net, x, y, nb_folds):
    # Splits the data into nb_folds batches using each batch as a testing set in turn
    nb_per_fold = math.ceil(len(y) / nb_folds)  # round up so last batch is smaller

    min_errs = []
    test_errs = []
    train_errs = []

    for i in range(nb_folds):
        print("--- Fold " + str(i+1) + " ---")

        net.reset()
        # Make test and training sets
        x_test = x[i*nb_per_fold:(i+1)*nb_per_fold]
        y_test = y[i*nb_per_fold:(i+1)*nb_per_fold]

        x_train = np.concatenate((x[:i*nb_per_fold], x[(i+1)*nb_per_fold:]), axis=0)
        y_train = np.concatenate((y[:i*nb_per_fold], y[(i+1)*nb_per_fold:]), axis=0)

        temp = net.test(x_train, y_train, 1500, 0.20, X_test=x_test, y_test=y_test)

        min_errs.append(temp[0])
        test_errs.append(temp[1])
        train_errs.append(temp[2])

        net.testProbBuckets(x_train, y_train, X_test=x_test, y_test=y_test)

    print("\n----------")
    print(net, "\tNb folds:", nb_folds)
    print("Avg min:", sum(min_errs)/nb_folds, "\t\t\t", min_errs)
    print("Avg final test:", sum(test_errs)/nb_folds, "\t\t\t", test_errs)
    print("Avg final train:", sum(train_errs)/nb_folds, "\t\t\t", train_errs)

    return

def testRuns(net, n, x, y):
    # Runs n tests and finds the average errors
    # Each run is
    min_errs =[]
    test_errs = []
    train_errs = []
    for i in range(n):
        print("--- Run " + str(i+1) + " ---")
        net.reset()
        temp = net.test(x, y, 2000, 0.25, 0.3)

        min_errs.append(temp[0])
        test_errs.append(temp[1])
        train_errs.append(temp[2])
        net.testProbBuckets(x, y, 0.3)

    print("\n----------")
    print(net)
    print("Avg min:", sum(min_errs)/n, "\t\t\t", min_errs)
    print("Avg final test:", sum(test_errs)/n, "\t\t\t", test_errs)
    print("Avg final train:", sum(train_errs)/n, "\t\t\t", train_errs)

    return

if __name__ == '__main__':

    input = np.genfromtxt(
    'InputData2014-15_Final.csv',           # file name
    delimiter=',',          # column delimiter
    dtype='float64',        # data type
    filling_values=0,       # fill missing values with 0
    )
    random.seed()
    random.shuffle(input)
    x = input[:, 1:]
    y = input[:, 0]

    net = nn.NeuralNetwork(96, 32, 1, nb_hidden_layers=3, weight_decay=15)

    crossValidate(net, x, y, 10)

    #net.test(x, y, 2000, 0.2, 0.3)
    #net.graphCosts(5)

    plt.show()

