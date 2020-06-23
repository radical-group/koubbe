import numpy as np


def load_data():
    TargetFeaturesList = ['Sugar', 'Alcohol']    
    data = []
    
    for targetMetric in TargetFeaturesList:
        data_name = 'data_' + targetMetric + '.npy'
        with open(data_name, 'rb') as f:
            X_combined = np.load(f)
            y_combined = np.load(f)
            data.append(X_combined)
            data.append(y_combined)
            
        #print('Data sets for ' + data_name + ' have been loaded correctly')
        
    return data