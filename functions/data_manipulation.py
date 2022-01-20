# https://textbooks.math.gatech.edu/ila/projections.html
import numpy as np
import copy

# split data for training and testing 
def split_data(Xi, p):
    m, _ = Xi.shape
    #X_train = X[:, 0:int(p*n)]
    #X_test = X[:, int(p*n):n]
    # Take the first 85 samples of digit Xi for the train session 
    X_train = Xi[0:85, :]
    X_test = Xi[85:m,:]
    return X_train, X_test

# Extract digits from X, and order them in a dictionary by value
def organize_samples(X, I):
    m, _ = X.shape # m images with n pixels
    digit_dict = {}
    # initialize the digit_dict with an empty list for every number
    for i in range(0,10):
        digit_dict["X"+str(i)] = [] 
    # populate the lists with the corresponding images by using the labels
    for i in range(0, m):
        num = I[i,0]
        digit_dict["X"+str(num)].append(list(X[i,:]))
    # convert the lists to np array since mathematical operations will be done on them
    for i in range(0,10):
        digit_dict["X"+str(i)] = np.array(digit_dict["X"+str(i)])
    return digit_dict

"""
 organize data into three dictionaries digit_dict (dictionary of all digits ordered by value), test_train_dict(a dictionary of all digits
 split into a training and test set) and a svd_dict(the svd decomposition of the digits in the training dataset)
"""
def organize_data(X, I):
    digit_dict = organize_samples(X,I) 
    test_train_dict = {"X_train":{}, "X_test":{}}
    svd_dict = {"U":{}, "S":{}, "V":{}}
    for i in range(0,10):
        # defining training and test set dictionary inside the test_train_dict
        X_train, X_test = split_data(digit_dict["X"+str(i)], 0.80)
        test_train_dict["X_train"]["X"+str(i)] = X_train 
        test_train_dict["X_test"]["X"+str(i)] = X_test
        # svd for the training data
        U, S, V = np.linalg.svd(test_train_dict["X_train"]["X"+str(i)], full_matrices=False)
        svd_dict["U"]["U"+str(i)] = U
        svd_dict["S"]["S"+str(i)] = S
        svd_dict["V"]["V"+str(i)] = V
    return digit_dict, test_train_dict, svd_dict
    
def test_digit(svd_dict, y):
    dist = np.zeros((10,1)) # distance vector for the digits
    for i in range(0,10):
        # extracting the V matrix from data dictionary
        Vi = svd_dict["V"]["V"+str(i)]
        # calculating the orthogonal projection and the distances with norms
        dist[i,0] = np.linalg.norm(y - Vi.T @ (Vi @ y))
    return np.argmin(dist), dist

def test_accuracy(X_data, svd_dict, num_sample):
    np.random.seed(1)
    wrong = 0 # number of wrong classifications
    wrong_samples = {} # the wrong identified samples
    X_test = copy.copy(X_data) # copy the test data
    i = 0
    while i < num_sample:
        # choose a random number to test
        rand_int = np.random.randint(0,10)
        # shape of the test set of the chosen random number
        m, n = X_test["X"+str(rand_int)].shape
        # if we used up all the samples for digit skip this iteration and try another
        #print(str(m) + " " + str(n) + " " + str(rand_int))
        if m == 0:
            continue
        # choose a random test sample for the previously chosen number
        rand_sample = np.random.randint(0,m)
        y_test = X_test["X"+str(rand_int)][rand_sample,:]
        # delete that sample so that in the next iteration it isn't chosen again
        X_test["X"+str(rand_int)] = np.delete(X_test["X"+str(rand_int)], rand_sample, axis = 0)
        # test if the random sample is correctly identified
        out, dist = test_digit(svd_dict, y_test) 
        if out != rand_int:
            wrong_samples[wrong] = y_test
            wrong+=1
        i = i + 1
    return (1- wrong/num_sample)*100, wrong_samples
        
     





