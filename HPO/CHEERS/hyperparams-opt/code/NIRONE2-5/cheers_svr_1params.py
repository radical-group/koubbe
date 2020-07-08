import argparse
import numpy as np

from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

from hyperspace import hyperdrive
from hyperspace.kepler import load_results


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

dataset = load_data()
X, y = dataset[0], dataset[1]   # Alcohol

reg = SVR()


def objective(params):
    """
    Objective function to be minimized.

    Parameters
    ----------
    * params [list, len(params)=n_hyperparameters]
        Settings of each hyperparameter for a given optimization iteration.
        - Controlled by hyperspaces's hyperdrive function.
        - Order preserved from list passed to hyperdrive's hyperparameters argument.
     """
    C = params

    reg.set_params(C=C)

    return -np.mean(cross_val_score(reg, X, y, cv=9, n_jobs=-1,
                    scoring="neg_mean_squared_error"))

def main():
    parser = argparse.ArgumentParser(description='CHEERS hyperparameter optimization')
    parser.add_argument('--results', type=str, help='Path to results directory.')
    args = parser.parse_args()

    hparams = [(0.1, 1000)]         # C

    hyperdrive(objective=objective,
               hyperparameters=hparams,
               results_path=args.results,
               checkpoints_path=args.results,
               model="GP",
               n_iterations=100,
               verbose=True,
               random_state=0)


if __name__=='__main__':
     main()