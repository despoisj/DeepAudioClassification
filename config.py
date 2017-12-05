#Define paths for files
spectrogramsInputPath = "Input/InputSpectrograms/"
spectrogramsPath = "Data/Spectrograms/"
slicesPath = "Data/Slices/"
slicesInputPath = "Input/Slices/"
datasetPath = "Data/Dataset/"
inputDatasetPath = "Input/Dataset/"
rawDataPath = "Data/Raw/"
inputDataPath = "Input/Raw/"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128

#Dataset parameters
filesPerGenre = 1000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.001
nbEpoch = 20