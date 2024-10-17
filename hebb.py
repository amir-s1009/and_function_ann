weights = [0 ,0]
bias = [0]

samples = []

def train(train_x_vector, target):
    try:
        #iterate over all of neurons and update weights & bias:
        for i in range(len(weights)):
            weights[i] += (train_x_vector[i] * target)

        bias[0] += target

        samples.append({'x1':train_x_vector[0], 'x2':train_x_vector[1], 't':target})

        # end of updating weights & bias
        return 1
    except:
        return 0

def test(test_x_vector):
    Yin = test_x_vector[0]*weights[0]+test_x_vector[1]*weights[1]+bias[0]
    if not weights[0] and not weights[1] and not bias[0]:
        return None
    elif Yin >= 0:
        return 1
    else:
        return -1
        