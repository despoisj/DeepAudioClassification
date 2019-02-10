#Define paths for files
spectrogramsPath = "Data/Spectrograms/"
slicesPath = "Data/Slices/"
datasetPath = "Data/Dataset/"
rawDataPath = "Data/Raw/"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128
sliceYSize = 256

#Dataset parameters
filesPerGenre = 10000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.001
nbEpoch = 20