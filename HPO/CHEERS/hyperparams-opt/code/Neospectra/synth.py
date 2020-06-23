import numpy as np
SYNTH_PERTURB_SIGNAL_FACTOR = 0.01
SYNTH_PERTURB_WAVELENGTHS_FACTOR = 0.1

def getNeoSynthFeatureDataIter(originalFeatureData):
    perturbedFeatureData = originalFeatureData
    numWavelengths = originalFeatureData.shape[1]
    numWavelengthsToPerturb = int(numWavelengths*SYNTH_PERTURB_WAVELENGTHS_FACTOR)
    for i in range(originalFeatureData.shape[0]):
        wavelengthsToPerturb = np.random.randint(0, numWavelengths, numWavelengthsToPerturb)
        for k in range(numWavelengthsToPerturb):
            ind = wavelengthsToPerturb[k]
            max_noise = perturbedFeatureData[i, ind] * SYNTH_PERTURB_SIGNAL_FACTOR
            distortion = np.random.uniform(-max_noise, max_noise)
            perturbedFeatureData[i, ind] = perturbedFeatureData[i, ind] + distortion
    return perturbedFeatureData


def getNeoSynthData(traininglDataMap, synthAdditionFactor):
    originalDataMap = traininglDataMap
    print('Original data set:', traininglDataMap['features'].shape, 'Adding synth data...')
    for i in range(synthAdditionFactor):
        for target in traininglDataMap:
            data = traininglDataMap[target]
            # Synthetic data to be added only for the feature information
            if target == 'features':
                syntheticData = getNeoSynthFeatureDataIter(originalDataMap['features'])
            else:
                syntheticData = originalDataMap[target]
            traininglDataMap[target] = np.concatenate((data, syntheticData), axis=0)
    print('Synthetic data addition complete. New data set:', traininglDataMap['features'].shape)
    return traininglDataMap
