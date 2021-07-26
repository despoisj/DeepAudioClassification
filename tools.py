# -*- coding: utf-8 -*-
import os
from PIL import Image
from random import shuffle
import numpy as np
import pickle

#Remove logs
import eyed3
eyed3.log.setLevel("ERROR")

from tools import get_image_data
from config import dataset_path, slices_path


### Audio tools ###
def is_mono(filename):
    audiofile = eyed3.load(filename)
    return audiofile.info.mode == 'Mono'

def get_genre(filename):
    audiofile = eyed3.load(filename)
    #No genre
    if not audiofile.tag.genre:
        return None
    else:
        return audiofile.tag.genre.name.encode('utf-8')


### Image tools ###
def get_processed_data(img, img_size):
    """Returns numpy image at size img_size*img_size"""
    img = img.resize((img_size, img_size), resample=Image.ANTIALIAS)
    img_data = np.asarray(img, dtype=np.uint8).reshape(img_size, img_size, 1)
    img_data = img_data / 255.
    return img_data

def get_image_data(filename, img_size):
    """Returns numpy image at size img_size * img_size"""
    img = Image.open(filename)
    img_data = get_processed_data(img, img_size)
    return img_data

### Dataset tools ###
def get_dataset_name(nb_per_genre, slice_size):
    """Creates name of dataset from parameters"""
    name = "{}".format(nb_per_genre)
    name += "_{}".format(slice_size)
    return name


def get_dataset(nb_per_genre, genres, slice_size, validation_ratio, test_ratio, mode):
    """Creates or loads dataset if it exists, note: Mode is train or test"""
    print("[+] Dataset name: {}".format(get_dataset_name(nb_per_genre, slice_size)))
    if not os.path.isfile(dataset_path + "train_X_" + get_dataset_name(nb_per_genre, slice_size) + ".p"):
        print("[+] Creating dataset with {} slices of size {} per genre... ⌛️".format(nb_per_genre, slice_size))
        create_dataset_from_slices(nb_per_genre, genres, slice_size, validation_ratio, test_ratio) 
    else:
        print("[+] Using existing dataset")
    
    return load_dataset(nb_per_genre, genres, slice_size, mode)
        

def load_dataset(nb_per_genre, genres, slice_size, mode):
    #Load existing
    dataset_name = get_dataset_name(nb_per_genre, slice_size)
    if mode == "train":
        print("[+] Loading training and validation datasets... ")
        train_X = pickle.load(open("{}train_X_{}.p".format(dataset_path,dataset_name), "rb" ))
        train_y = pickle.load(open("{}train_y_{}.p".format(dataset_path,dataset_name), "rb" ))
        validation_X = pickle.load(open("{}validation_X_{}.p".format(dataset_path,dataset_name), "rb" ))
        validation_y = pickle.load(open("{}validation_y_{}.p".format(dataset_path,dataset_name), "rb" ))
        print("    Training and validation datasets loaded! ✅")
        return train_X, train_y, validation_X, validation_y

    else:
        print("[+] Loading testing dataset... ")
        test_X = pickle.load(open("{}test_X_{}.p".format(dataset_path,dataset_name), "rb" ))
        test_y = pickle.load(open("{}test_y_{}.p".format(dataset_path,dataset_name), "rb" ))
        print("    Testing dataset loaded! ✅")
        return test_X, test_y


def save_dataset(train_X, train_y, validation_X, validation_y, test_X, test_y, nb_per_genre, genres, slice_size):
    #Create path for dataset if doesn't exist
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

    #save_dataset
    print("[+] Saving dataset... ")
    dataset_name = get_dataset_name(nb_per_genre, slice_size)
    pickle.dump(train_X, open("{}train_X_{}.p".format(dataset_path,dataset_name), "wb" ))
    pickle.dump(train_y, open("{}train_y_{}.p".format(dataset_path,dataset_name), "wb" ))
    pickle.dump(validation_X, open("{}validation_X_{}.p".format(dataset_path,dataset_name), "wb" ))
    pickle.dump(validation_y, open("{}validation_y_{}.p".format(dataset_path,dataset_name), "wb" ))
    pickle.dump(test_X, open("{}test_X_{}.p".format(dataset_path,dataset_name), "wb" ))
    pickle.dump(test_y, open("{}test_y_{}.p".format(dataset_path,dataset_name), "wb" ))
    print("    Dataset saved! ✅💾")


def create_dataset_from_slices(nb_per_genre, genres, slice_size, validation_ratio, test_ratio):
    """Creates and save dataset from slices"""
    data = []
    for genre in genres:
        print("-> Adding {}...".format(genre))
        #Get slices in genre subfolder
        filenames = os.listdir(slices_path + genre)
        filenames = [filename for filename in filenames if filename.endswith('.png')]
        filenames = filenames[:nb_per_genre]
        #Randomize file selection for this genre
        shuffle(filenames)

        #Add data (X,y)
        for filename in filenames:
            img_data = get_image_data(slices_path + genre + "/" + filename, slice_size)
            label = [1. if genre == g else 0. for g in genres]
            data.append((img_data,label))

    #Shuffle data
    shuffle(data)

    #Extract X and y
    X,y = zip(*data)

    #Split data
    validation_nb = int(len(X) * validation_ratio)
    test_nb = int(len(X) * test_ratio)
    train_nb = len(X) - (validation_nb + test_nb)

    #Prepare for Tflearn at the same time
    train_X = np.array(X[:train_nb]).reshape([-1, slice_size, slice_size, 1])
    train_y = np.array(y[:train_nb])
    validation_X = np.array(X[train_nb:train_nb+validation_nb]).reshape([-1, slice_size, slice_size, 1])
    validation_y = np.array(y[train_nb:train_nb+validation_nb])
    test_X = np.array(X[-test_nb:]).reshape([-1, slice_size, slice_size, 1])
    test_y = np.array(y[-test_nb:])
    print("    Dataset created! ✅")
        
    #Save
    save_dataset(train_X, train_y, validation_X, validation_y, test_X, test_y, nb_per_genre, genres, slice_size)

    return train_X, train_y, validation_X, validation_y, test_X, test_y
