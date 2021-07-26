# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import numpy as np

from model import create_model
from tools import get_dataset
from config import slices_path, slice_size, batch_size, files_per_genre, nb_epochs
from config import validation_ratio, test_ratio
from song_to_data import create_slices_from_audio

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice"])
args = parser.parse_args()

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validation_ratio))
print("| Test ratio: {}".format(test_ratio))
print("| Slices per genre: {}".format(files_per_genre))
print("| Slice size: {}".format(slice_size))
print("--------------------------")

if __name__ == "__main__":
	if "slice" in args.mode:
		create_slices_from_audio()
		sys.exit()

	#List genres
	genres = os.listdir(slices_path)
	genres = [filename for filename in genres if os.path.isdir(slices_path + filename)]
	nb_classes = len(genres)

	#Create model 
	model = create_model(nb_classes, slice_size)

	# Noe: We can do both train and test at once
	if "train" in args.mode:

		#Create or load new dataset
		train_X, train_y, validation_X, validation_y = get_dataset(files_per_genre, genres, slice_size, validation_ratio, test_ratio, mode="train")

		#Define run id for graphs
		run_id = "MusicGenres - " + str(batch_size) + " " + ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

		#Train the model
		print("[+] Training the model...")
		model.fit(train_X, train_y, n_epoch=nb_epochs, batch_size=batch_size, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
		print("    Model trained! ✅")

		#Save trained model
		print("[+] Saving the weights...")
		model.save('musicDNN.tflearn')
		print("[+] Weights saved! ✅💾")

	if "test" in args.mode:

		#Create or load new dataset
		test_X, test_y = get_dataset(files_per_genre, genres, slice_size, validation_ratio, test_ratio, mode="test")

		#Load weights
		print("[+] Loading weights...")
		model.load('musicDNN.tflearn')
		print("    Weights loaded! ✅")

		testAccuracy = model.evaluate(test_X, test_y)[0]
		print("[+] Test accuracy: {} ".format(testAccuracy))
