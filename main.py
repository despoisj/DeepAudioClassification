# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import numpy as np
import operator

from model import createModel
from datasetTools import getDataset, getInputDataset
from config import slicesPath
from config import batchSize
from config import filesPerGenre
from config import nbEpoch
from config import validationRatio, testRatio
from config import sliceSize

from songToData import createSlicesFromAudio, createSlicesFromInputAudio

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice", "predict", "sliceInput"])
args = parser.parse_args()

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validationRatio))
print("| Test ratio: {}".format(testRatio))
print("| Slices per genre: {}".format(filesPerGenre))
print("| Slice size: {}".format(sliceSize))
print("--------------------------")

if "slice" in args.mode:
	createSlicesFromAudio()
	sys.exit()

if "sliceInput" in args.mode:
	createSlicesFromInputAudio()
	sys.exit()

#List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]
nbClasses = len(genres)

#Create model 
model = createModel(nbClasses, sliceSize)

if "train" in args.mode:

	#Create or load new dataset
	train_X, train_y, validation_X, validation_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

	#Define run id for graphs
	run_id = "MusicGenres - "+str(batchSize)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

	#Train the model
	print("[+] Training the model...")
	model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
	print("    Model trained! ✅")

	#Save trained model
	print("[+] Saving the weights...")
	model.save('musicDNN.tflearn')
	print("[+] Weights saved! ✅💾")

if "test" in args.mode:

	#Create or load new dataset
	test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")

	#Load weights
	print("[+] Loading weights...")
	model.load('musicDNN.tflearn')
	print("    Weights loaded! ✅")

	testAccuracy = model.evaluate(test_X, test_y)[0]
	print("[+] Test accuracy: {} ".format(testAccuracy))

if "predict" in args.mode:
	# Create or load new dataset
	inp_X, inp_y = getInputDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")

	model.load('musicDNN.tflearn')

	countArray = [0,0,0,0,0,0,0,0,0,0]
	genreCountDict = dict(zip(genres,countArray))

	for i in range(len(inp_X)):
		prediction = model.predict([inp_X[i]])
		maxIndex, maxValue = max(enumerate(prediction[0]), key=operator.itemgetter(1))
		tempValue = genreCountDict[genres[maxIndex]]
		tempValue = tempValue + 1
		genreCountDict[genres[maxIndex]] = tempValue

	predictedGenre = max(genreCountDict.iteritems(), key=operator.itemgetter(1))[0]
	print (genreCountDict)
	print (predictedGenre)






