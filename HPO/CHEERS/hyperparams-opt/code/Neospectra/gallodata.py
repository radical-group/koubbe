import numpy as np
import pandas as pd
from dateutil.parser import parse


def test():
	print("Hello World")
def generateGroundTruthSheet(filename, sheet, groundTruthMap):
	# Read the Optimal Solutions Data Set from ASL excel file
    groundTruth = pd.read_excel(open(filename, 'rb'), sheet_name=sheet)
	# Convert the table into array
    gt = groundTruth.reset_index().values
	# Get the A420, A520, alcohol, sugar and tannins contents for every sample with it's date  
    for i in range(gt.shape[0]):
        subdate = gt[i, 2]
        if type(subdate) is str:
            subdate = parse(gt[i, 2]).date()
        else:
            subdate = gt[i, 2].date()
        if subdate not in groundTruthMap:
            groundTruthMap[subdate] = {}
        tankNumber = int(gt[i, 1])
        if tankNumber not in groundTruthMap[subdate]:
            groundTruthMap[subdate][tankNumber] = {}
        groundTruthMap[subdate][tankNumber]['A420'] = gt[i, 3]
        groundTruthMap[subdate][tankNumber]['A520'] = gt[i, 4]
        groundTruthMap[subdate][tankNumber]['Alcohol'] = gt[i, 5]
        groundTruthMap[subdate][tankNumber]['Sugar'] = gt[i, 6]
        groundTruthMap[subdate][tankNumber]['Tannins'] = gt[i, 7]
    return groundTruthMap

'''	Output : {datetime.date(2017, 9, 26): {772: {'A420': 4.799, 'A520': 14.06, 'Alcohol': 11.48, 'Sugar': 3.7, 'Tannins': 2209}, 
	            773: {'A420': 4.663, 'A520': 11.32, 'Alcohol': 11.18, 'Sugar': 4.19, 'Tannins': 2061} cont....
'''


def generateGroundTruth(filename, groundTruthMap):
    print('Generating ground truth')
	# Store all the sheetnames (dates) in sheetNames
    sheetNames = pd.ExcelFile(filename).sheet_names
    print('sheetnames:', sheetNames)
	# For every date (sheetNames) do the following
    for sheet in sheetNames:
        print('processing sheet:', sheet)
        generateGroundTruthSheet(filename, sheet, groundTruthMap)
    return groundTruthMap


def generateGroundTruthInnoculationSheet(filename, sheet, groundTruthMap):
    print('Sheetname:', sheet)
    groundTruth = pd.read_excel(open(filename, 'rb'), sheet_name=sheet)
    gt = groundTruth.reset_index().values
    for i in range(gt.shape[0]):
        subdate = sheet  # gt[i,2]
        if type(subdate) is str:
            subdate = parse(subdate).date()
        else:
            subdate = subdate.date()
        tankNumber = int(gt[i, 1])
        innoculationDate = gt[i, 5]
        if type(innoculationDate) is str:
            print('subdate:', innoculationDate)
            innoculationDate = parse(innoculationDate).date()
        else:
            innoculationDate = innoculationDate.date()
        if subdate not in groundTruthMap:  # groundTruthInnoculationMap:
            groundTruthMap[subdate] = {}  # groundTruthInnoculationMap[subdate] = {}
        daysInoculation = (subdate - innoculationDate).days
        if tankNumber not in groundTruthMap[subdate]:
            groundTruthMap[subdate][tankNumber] = {}
        groundTruthMap[subdate][tankNumber]['Inoculation'] = daysInoculation
    return groundTruthMap


def generateGroundTruthInnoculation(filename, groundTruthMap):
    print('Generating ground truth for inoculation days')
    sheetNames = pd.ExcelFile(filename).sheet_names
    print('sheetnames:', sheetNames)
    for sheet in sheetNames:
        print('processing sheet:', sheet)
        generateGroundTruthInnoculationSheet(filename, sheet, groundTruthMap)
    return groundTruthMap


def generateGroundTruthGrapeColorSheet(filename, sheet, groundTruthMap):
    groundTruth = pd.read_excel(open(filename, 'rb'), sheet_name=sheet)
    gt = groundTruth.reset_index().values
    for i in range(gt.shape[0]):
        subdate = sheet
        if type(subdate) is str:
            subdate = parse(subdate).date()
        else:
            subdate = subdate.date()
        tankNumber = int(gt[i, 1])
        if subdate not in groundTruthMap:
            groundTruthMap[subdate] = {}
        grapeColor = gt[i, 4]
        varietal = gt[i, 3]
        if tankNumber not in groundTruthMap[subdate]:
            groundTruthMap[subdate][tankNumber] = {}
        groundTruthMap[subdate][tankNumber]['Color'] = grapeColor
        groundTruthMap[subdate][tankNumber]['Varietal'] = varietal
    return groundTruthMap


def generateGroundTruthGrapeColorMap(filename, groundTruthMap):
    print('Generating ground truth map for grape color')
    sheetNames = pd.ExcelFile(filename).sheet_names
    print('sheetnames:', sheetNames)
    for sheet in sheetNames:
        print('processing sheet:', sheet)
        generateGroundTruthGrapeColorSheet(filename, sheet, groundTruthMap)
    return groundTruthMap


'''	The following function returns true if the wine is red (determined by Optimal Solutions Data Set and gallo(date) excel files)
	and false if the wine is not red
'''
def includeInData(groundTruthMap, code, sampledate):
    # return True
    if code == 780:
        return False

    if code == 621:
        code = 622
    if code == 721:
        code = 722

#     if groundTruthMap[sampledate][code]['Color'] == colorChoice and groundTruthMap[sampledate][code]['Varietal'] == 'Pinot Noir':
    try:
        c = groundTruthMap[sampledate][code]['Color']
    except:
        #print(sampledate, code)
        return False
    # if 'cabernet' in groundTruthMap[sampledate][code]['Varietal'].lower():
    if 'red' in groundTruthMap[sampledate][code]['Color'].lower():
        return True
    else:
        return False

'''
This function returns the corresponding value for the red wine samples
'''
def getGroundTruthForCode(groundTruthMap, code, sampledate, blindTestMode):
    if code == 621:
        code = 622
    if code == 721:
        code = 722
    labelsMap = {}
    labelsMap['Tank'] = code
    if blindTestMode:
        labelsMap['A420'] = 0
        labelsMap['A520'] = 0
        labelsMap['Alcohol'] = 0
        labelsMap['Sugar'] = 0
        labelsMap['Tannins'] = 0
        labelsMap['Inoculation'] = 0
        labelsMap['Color'] = 0
        return labelsMap

    labelsMap['A420'] = groundTruthMap[sampledate][code]['A420']
    labelsMap['A520'] = groundTruthMap[sampledate][code]['A520']
    labelsMap['Alcohol'] = groundTruthMap[sampledate][code]['Alcohol']
    labelsMap['Sugar'] = groundTruthMap[sampledate][code]['Sugar']
    labelsMap['Tannins'] = groundTruthMap[sampledate][code]['Tannins']
    labelsMap['Inoculation'] = groundTruthMap[sampledate][code]['Inoculation']
    labelsMap['Color'] = groundTruthMap[sampledate][code]['Color']
    return labelsMap

def getNeospectraDataFromFile(groundTruthMap, filename, subdate, blindTestMode):
	# numpyData contains the matrix of all the sample names and its level of absorption
    numpyData = pd.read_csv(filename).to_numpy()
	# xDataFull contains the level of absorption
    xDataFull = numpyData[:,1:].astype('float')
	# strData contains the sample names
    strData = numpyData[:,0]
    xData = None
    yTank = None
    yA420 = None
    yA520 = None
    yAlcohol = None
    ySugar = None
    yTannins = None
    yInoculation = None
    sampledate = parse(subdate).date()

    datapoints = 0
    excludedPoints = 0
    for i in range(strData.shape[0]):
        if '8nm' in strData[i]:
            code = int(strData[i].split('-')[0])
        else:
		# Split the sample name. For example: 613Raw_Abs_1.Spectrum converted to 613
            code = int(strData[i].split('Raw')[0])
		
		# If the includeInData function returns true i.e, if the sample is red wine then we increment the datapoints by 1
		# If function returns false then we increment the excludedPoints by 1 and immediately go to the next sample and continue the process 
        if not includeInData(groundTruthMap, code, sampledate):
            excludedPoints += 1
            continue
					
		# If it is red wine then do the following steps 
        datapoints += 1
		# Select the level of absorption for that sample (1D array)
        x = xDataFull[i,:].reshape(([1,-1]))
		# Get all the corresponding values for the sample
        labelsMap = getGroundTruthForCode(groundTruthMap, code, sampledate, blindTestMode)
        yTankLabel = np.array(([labelsMap['Tank']]))
        yA420Sample = np.array(([labelsMap['A420']]))
        yA520Sample = np.array(([labelsMap['A520']]))
        yAlcoholSample = np.array(([labelsMap['Alcohol']]))
        ySugarSample = np.array(([labelsMap['Sugar']]))
        yTanninsSample = np.array(([labelsMap['Tannins']]))
        yInoculationSample = np.array(([labelsMap['Inoculation']]))
        if xData is None:
            xData = x
            yTank = yTankLabel
            yA420 = yA420Sample
            yA520 = yA520Sample
            yAlcohol = yAlcoholSample
            ySugar = ySugarSample
            yTannins = yTanninsSample
            yInoculation = yInoculationSample
        else:
            xData = np.concatenate((xData, x), axis=0)
            yTank = np.concatenate((yTank, yTankLabel), axis=0)
            yA420 = np.concatenate((yA420, yA420Sample), axis=0)
            yA520 = np.concatenate((yA520, yA520Sample), axis=0)
            yAlcohol = np.concatenate((yAlcohol, yAlcoholSample), axis=0)
            ySugar = np.concatenate((ySugar, ySugarSample), axis=0)
            yTannins = np.concatenate((yTannins, yTanninsSample), axis=0)
            yInoculation = np.concatenate((yInoculation, yInoculationSample), axis=0)
#   The Datapoints represents the number of samples which are red wine for particular subdate 
#	The excludedPoints represents the number of samples which are white wine for particular subdate
    print('Datapoints:', datapoints, 'Excluded points:', excludedPoints)
    return xData, yTank, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation

def getNeospectraDataFromFiles(groundTruthMap, filenameMap, blindTestMode=False):
    xDataAll = None
    yTankAll = None
    yA420All = None
    yA520All = None
    yAlcoholAll = None
    ySugarAll = None
    yTanninsAll = None
    yInoculationAll = None

    for subdate in filenameMap:
		# Reading the training data file name for each subdate
        filename = filenameMap[subdate]
        print('Reading data from:', filename, subdate)
        xData, yTank, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation = getNeospectraDataFromFile(groundTruthMap, filename, subdate, blindTestMode)
        if xDataAll is None:
            xDataAll = xData
            yTankAll = yTank
            yA420All = yA420
            yA520All = yA520
            yAlcoholAll = yAlcohol
            ySugarAll = ySugar
            yTanninsAll = yTannins
            yInoculationAll = yInoculation
        else:
            xDataAll = np.concatenate((xDataAll, xData), axis=0)
            yTankAll = np.concatenate((yTankAll, yTank), axis=0)
            yA420All = np.concatenate((yA420All, yA420), axis=0)
            yA520All = np.concatenate((yA520All, yA520), axis=0)
            yAlcoholAll = np.concatenate((yAlcoholAll, yAlcohol), axis=0)
            ySugarAll = np.concatenate((ySugarAll, ySugar), axis=0)
            yTanninsAll = np.concatenate((yTanninsAll, yTannins), axis=0)
            yInoculationAll = np.concatenate((yInoculationAll, yInoculation), axis=0)
    extractedData = {}
    extractedData['features'] = xDataAll
    extractedData['Tank'] = yTankAll
    if blindTestMode:
        return extractedData
    extractedData['A420'] = yA420All
    extractedData['A520'] = yA520All
    extractedData['Alcohol'] = yAlcoholAll
    extractedData['Sugar'] = ySugarAll
    extractedData['Tannins'] = yTanninsAll
    extractedData['Inoculation'] = yInoculationAll
    return extractedData
	
	# It contains all the red wine sample records 

def getMicroNIRDataFromFile(groundTruthMap, filename, subdate):
    numpyData = pd.read_excel(open(filename, 'rb'), sheet_name=0).reset_index().to_numpy()
    xDataFull = numpyData[:, 1:-3].astype('float')
    strData = numpyData[:, 0]

    xData = None
    yA420 = None
    yA520 = None
    yAlcohol = None
    ySugar = None
    yTannins = None
    yInoculation = None
    sampledate = parse(subdate).date()

    datapoints = 0
    for i in range(strData.shape[0]):
        code = int(strData[i].split('-')[0].split('Raw')[0])
        if not includeInData(groundTruthMap, code, sampledate):
            continue
        datapoints += 1
        x = xDataFull[i,:].reshape(([1,-1]))
        labelsMap = getGroundTruthForCode(groundTruthMap, code, sampledate)
        yTankSample = np.array(([labelsMap['Tank']]))
        yA420Sample = np.array(([labelsMap['A420']]))
        yA520Sample = np.array(([labelsMap['A520']]))
        yAlcoholSample = np.array(([labelsMap['Alcohol']]))
        ySugarSample = np.array(([labelsMap['Sugar']]))
        yTanninsSample = np.array(([labelsMap['Tannins']]))
        yInoculationSample = np.array(([labelsMap['Inoculation']]))
        if xData is None:
            xData = x
            yTank = yTankSample
            yA420 = yA420Sample
            yA520 = yA520Sample
            yAlcohol = yAlcoholSample
            ySugar = ySugarSample
            yTannins = yTanninsSample
            yInoculation = yInoculationSample
        else:
            xData = np.concatenate((xData, x), axis=0)
            yTank = np.concatenate((yTank, yTankSample), axis=0)
            yA420 = np.concatenate((yA420, yA420Sample), axis=0)
            yA520 = np.concatenate((yA520, yA520Sample), axis=0)
            yAlcohol = np.concatenate((yAlcohol, yAlcoholSample), axis=0)
            ySugar = np.concatenate((ySugar, ySugarSample), axis=0)
            yTannins = np.concatenate((yTannins, yTanninsSample), axis=0)
            yInoculation = np.concatenate((yInoculation, yInoculationSample), axis=0)
    print('Datapoints:', datapoints)
    return xData, yTank, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation

def getMicroNIRDataFromFiles(groundTruthMap, filenameMap):
    xDataAll = None
    yTankAll = None
    yA420All = None
    yA520All = None
    yAlcoholAll = None
    ySugarAll = None
    yTanninsAll = None
    yInoculationAll = None

    for subdate in filenameMap:
        filename = filenameMap[subdate]
        print('Reading date from:', filename, subdate)
        xData, yTank, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation = getMicroNIRDataFromFile(groundTruthMap, filename, subdate)
        if xDataAll is None:
            xDataAll = xData
            yTankAll = yTank
            yA420All = yA420
            yA520All = yA520
            yAlcoholAll = yAlcohol
            ySugarAll = ySugar
            yTanninsAll = yTannins
            yInoculationAll = yInoculation
        else:
            xDataAll = np.concatenate((xDataAll, xData), axis=0)
            yTankAll = np.concatenate((yTankAll, yTank), axis=0)
            yA420All = np.concatenate((yA420All, yA420), axis=0)
            yA520All = np.concatenate((yA520All, yA520), axis=0)
            yAlcoholAll = np.concatenate((yAlcoholAll, yAlcohol), axis=0)
            ySugarAll = np.concatenate((ySugarAll, ySugar), axis=0)
            yTanninsAll = np.concatenate((yTanninsAll, yTannins), axis=0)
            yInoculationAll = np.concatenate((yInoculationAll, yInoculation), axis=0)
    extractedData = {}
    extractedData['features'] = xDataAll
    extractedData['Tank'] = yTankAll
    extractedData['A420'] = yA420All
    extractedData['A520'] = yA520All
    extractedData['Alcohol'] = yAlcoholAll
    extractedData['Sugar'] = ySugarAll
    extractedData['Tannins'] = yTanninsAll
    extractedData['Inoculation'] = yInoculationAll
    return extractedData

def getScioDataFromFile(groundTruthMap, filename, subdate):
    numpyData = pd.read_excel(open(filename, 'rb'), sheet_name=0).reset_index().to_numpy()
    rowIndex = -1
    for i in range(numpyData.shape[0]):
        if 'id' in str(numpyData[i, 1]):
            rowIndex = i
            break

    sampleRow = numpyData[rowIndex, :].reshape([1,-1]).astype('str')
    tankIndex = -1
    spectraIndex = -1
    for i in range(sampleRow.shape[1]):
        if 'tank' in sampleRow[0,i].lower():
            tankIndex = i
            break
    for i in range(sampleRow.shape[1]):
        if 'spectrum' in sampleRow[0,i]:
            spectraIndex = i
            break
    print('SCiO file indices:', rowIndex, tankIndex, spectraIndex)

    xDataFull = numpyData[11:, spectraIndex:].astype('float')
    strData = numpyData[11:, tankIndex]

    xData = None
    yA420 = None
    yA520 = None
    yAlcohol = None
    ySugar = None
    yTannins = None
    yInoculation = None
    sampledate = parse(subdate).date()

    datapoints = 0
    for i in range(strData.shape[0]):
        code = int(strData[i]) #.split('-')[0].split('Raw')[0])
        if not includeInData(groundTruthMap, code, sampledate):
            continue
        datapoints += 1
        x = xDataFull[i,:].reshape(([1,-1]))
        labelsMap = getGroundTruthForCode(groundTruthMap, code, sampledate)
        yA420Sample = np.array(([labelsMap['A420']]))
        yA520Sample = np.array(([labelsMap['A520']]))
        yAlcoholSample = np.array(([labelsMap['Alcohol']]))
        ySugarSample = np.array(([labelsMap['Sugar']]))
        yTanninsSample = np.array(([labelsMap['Tannins']]))
        yInoculationSample = np.array(([labelsMap['Inoculation']]))
        if xData is None:
            xData = x
            yA420 = yA420Sample
            yA520 = yA520Sample
            yAlcohol = yAlcoholSample
            ySugar = ySugarSample
            yTannins = yTanninsSample
            yInoculation = yInoculationSample
        else:
            xData = np.concatenate((xData, x), axis=0)
            yA420 = np.concatenate((yA420, yA420Sample), axis=0)
            yA520 = np.concatenate((yA520, yA520Sample), axis=0)
            yAlcohol = np.concatenate((yAlcohol, yAlcoholSample), axis=0)
            ySugar = np.concatenate((ySugar, ySugarSample), axis=0)
            yTannins = np.concatenate((yTannins, yTanninsSample), axis=0)
            yInoculation = np.concatenate((yInoculation, yInoculationSample), axis=0)
    print('Datapoints:', datapoints)
    return  xData, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation

def getScioDataFromFiles(groundTruthMap, filenameMap):
    xDataAll = None
    yA420All = None
    yA520All = None
    yAlcoholAll = None
    ySugarAll = None
    yTanninsAll = None
    yInoculationAll = None

    for subdate in filenameMap:
        filename = filenameMap[subdate]
        print('Reading date from:', filename, subdate)
        xData, yA420, yA520, yAlcohol, ySugar, yTannins, yInoculation = getScioDataFromFile(groundTruthMap, filename, subdate)
        if xDataAll is None:
            xDataAll = xData
            yA420All = yA420
            yA520All = yA520
            yAlcoholAll = yAlcohol
            ySugarAll = ySugar
            yTanninsAll = yTannins
            yInoculationAll = yInoculation
        else:
            xDataAll = np.concatenate((xDataAll, xData), axis=0)
            yA420All = np.concatenate((yA420All, yA420), axis=0)
            yA520All = np.concatenate((yA520All, yA520), axis=0)
            yAlcoholAll = np.concatenate((yAlcoholAll, yAlcohol), axis=0)
            ySugarAll = np.concatenate((ySugarAll, ySugar), axis=0)
            yTanninsAll = np.concatenate((yTanninsAll, yTannins), axis=0)
            yInoculationAll = np.concatenate((yInoculationAll, yInoculation), axis=0)
    extractedData = {}
    extractedData['features'] = xDataAll
    extractedData['A420'] = yA420All
    extractedData['A520'] = yA520All
    extractedData['Alcohol'] = yAlcoholAll
    extractedData['Sugar'] = ySugarAll
    extractedData['Tannins'] = yTanninsAll
    extractedData['Inoculation'] = yInoculationAll
    return extractedData
