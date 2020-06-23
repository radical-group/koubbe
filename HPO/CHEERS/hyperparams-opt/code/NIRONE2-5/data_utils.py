import numpy as np


def load_data():
    TargetFeaturesList = ['Alcohol']    
    data = []
    
    for targetMetric in TargetFeaturesList:
        data_name = 'data_' + targetMetric + '.npy'
        with open(data_name, 'rb') as f:
            X = np.load(f)
            y = np.load(f)
            data.append(X)
            data.append(y)
                
    return data