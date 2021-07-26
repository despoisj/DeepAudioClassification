#Define paths for files
spectrograms_path = "Data/Spectrograms/"
slices_path = "Data/Slices/"
dataset_path = "Data/Dataset/"
raw_data_path = "Data/Raw/"

#Spectrogram resolution
pixel_per_second = 50

#Slice parameters
slice_size = 128

#Dataset parameters
files_per_genre = 1000
validation_ratio = 0.3
test_ratio = 0.1

#Model parameters
batch_size = 128
learning_rate = 0.001
nb_epochs = 20