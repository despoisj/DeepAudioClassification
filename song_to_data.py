# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image

#Remove logs
import eyed3
eyed3.log.setLevel("ERROR")

from slice_spectrogram import create_slices_from_spectrograms
from tools import is_mono, get_genre
from config import raw_data_path, spectrograms_path, pixel_per_second, slice_size


def create_spectrogram(filename, new_filename):
	"""Creates spectrogram from mp3 files"""
	current_path = os.path.dirname(os.path.realpath(__file__)) 

	filepath = os.path.join(raw_data_path, filename)
	#Create temporary mono track if needed
	if is_mono(filepath):
		command = "cp '{}' '/tmp/{}.mp3'".format(filepath, new_filename)
	else:
		command = "sox '{}' '/tmp/{}.mp3' remix 1,2".format(filepath, new_filename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=current_path)
	output, errors = p.communicate()
	if errors:
		print errors

	#Create spectrogram
	spectrogram_filepath = os.path.join(spectrograms_path, new_filename)
	command = "sox '/tmp/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(new_filename, pixel_per_second, spectrogram_filepath)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=current_path)
	output, errors = p.communicate()
	if errors:
		print errors

	#Remove tmp mono track
	os.remove("/tmp/{}.mp3".format(new_filename))

def create_spectrograms_from_audio():
	"""Creates .png whole spectrograms from mp3 files"""
	genres_id = {}
	files = [file for file in os.listdir(raw_data_path) if file.endswith(".mp3")]

	#Create path if doesn't exist
	os.makedirs(os.path.dirname(spectrograms_path), exist_ok=True)

	#Rename files according to genre
	for index, filename in enumerate(files):
		print "Creating spectrogram for file {}/{}...".format(index + 1, len(files))
		file_genre = get_genre(raw_data_path + filename)
		file_id = genres_id.get(file_genre, 0) + 1
		genres_id[file_genre] = file_id # Increment counter
		new_filename = file_genre + "_" + str(file_id)
		create_spectrogram(filename, new_filename)

def create_slices_from_audio():
	"""Whole pipeline .mp3 -> .png slices"""
	print "Creating spectrograms..."
	create_spectrograms_from_audio()
	print "Spectrograms created!"

	print "Creating slices..."
	create_slices_from_spectrograms(slice_size)
	print "Slices created!"
