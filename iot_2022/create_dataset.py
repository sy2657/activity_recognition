# max split

# Split
def create_dataset(X,Y):
    ''' CreateDataset: creates a training dataset and validation dataset
        Input: Directory with a collection of vectors of fixed dimension for each video
        Output: A training set (X_train,Y_train), a validation (X_test, Y_test)
        
    '''
    X_train = []
    X_test = []
    Y_train = []
    Y_train_numerical = []
    Y_test = []
    Y_test_numerical = []
    for i in range(len(X)):
        x_train,x_test,y_train,y_test = train_test_split(results[i],labels[i],test_size =0.3)
        for item in x_train:
            X_train.append(item)
        for item in y_train:

            Y_train.append(item)
            if item == 'no_interaction':
              Y_train_numerical.append(0)
            if item == 'open_close_fridge':
              Y_train_numerical.append(1)
            if item == 'put_back_item':
              Y_train_numerical.append(2)
            if item == 'screen_interaction':
              Y_train_numerical.append(3)
            if item == 'take_out_item':
              Y_train_numerical.append(4)
            #print(item)
            #break
            # numericalize it 
        for item in x_test:
            X_test.append(item)
        for item in y_test:
            Y_test.append(item)
            if item == 'no_interaction':
              Y_test_numerical.append(0)
            if item == 'open_close_fridge':
              Y_test_numerical.append(1)
            if item == 'put_back_item':
              Y_test_numerical.append(2)
            if item == 'screen_interaction':
              Y_test_numerical.append(3)
            if item == 'take_out_item':
              Y_test_numerical.append(4)

    maximum_x_train = float('-inf')
    for i in range(len(X_train)):
        n_x_train = np.array(X_train[i]).shape[0]
        maximum_x_train = max(maximum_x_train,n_x_train)
    maximum_x_test = float('-inf')
    for i in range(len(X_test)):
        n_x_test = np.array(X_test[i]).shape[0]
        maximum_x_test = max(maximum_x_train,n_x_test)

    if maximum_x_test < maximum_x_train:
        for i in range(len(X_test)):
            for m in range(len(X_test[i]),maximum_x_train+1):
                 print(np.array(X_test[i]).shape)
                 X_test[i].append(np.zeros((3,17)))
        for i in range(len(X_train)):
            for m in range(len(X_train[i]),maximum_x_train+1):
                 X_train[i].append(np.zeros((3,17)))
    else:
        for i in range(len(X_test)):
            for m in range(len(X_test[i]),maximum_x_test+1):
                 X_test[i].append(np.zeros((3,17)))
        for i in range(len(X_train)):
            for m in range(len(X_train[i]),maximum_x_test+1):
                 X_train[i].append(np.zeros((3,17)))
     
    return (X_train, Y_train_numerical), (X_test, Y_test_numerical)
