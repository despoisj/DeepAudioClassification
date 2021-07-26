# Import Pillow:
from PIL import Image
import os.path

from config import spectrograms_path, slices_path


def create_slices_from_spectrograms(desired_size):
	"""Batch slicing"""
	spectrograms = [f for f in os.listdir(spectrograms_path) if f.endswith(".png")]
	for spectrogram in spectrograms:
		slice_spectrogram(filename,desired_size)


#TODO Improvement - Make sure we don't miss the end of the song
def slice_spectrogram(filename, desired_size):
	"""Creates slices from one spectrogram"""
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(spectrograms_path + filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nb_samples = int(width / desired_size)
	width - desired_size

	#Create path if doesn't exist
	slice_path = slices_path + "{}/".format(genre);
	os.makedirs(os.path.dirname(slice_path), exist_ok=True)

	#For each sample
	for i in range(nb_samples):
		print "Creating slice: ", i + 1, "/", nb_samples, "for", filename
		#Extract and save 128x128 sample
		startPixel = i * desired_size
		img_tmp = img.crop((startPixel, 1, startPixel + desired_size, desired_size + 1))
		img_tmp.save(slices_path + "{}/{}_{}.png".format(genre, filename[:-4], i))
