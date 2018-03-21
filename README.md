# Deep Audio Classification
A pipeline to build a dataset from your own music library and use it to fill the missing genres

Read the [article on Medium](https://medium.com/@juliendespois/finding-the-genre-of-a-song-with-deep-learning-da8f59a61194#.yhemoyql0)

Required install:

```
eyed3
sox --with-lame
tensorflow
tflearn
```

- Create folder Data/Raw/
- Place your labeled .mp3 files in Data/Raw/

To create the song slices (might be long):

```
python main.py slice
```

To train the classifier (long too):

```
python main.py train
```

To test the classifier (fast):

```
python main.py test
```

- Create folder Input/Raw/
- Place your unlabeled .mp3 files in Input/Raw/

To create song slices of song to predict:

```
python main.py sliceInput
```

To predict the classifier's output:

```
python main.py predict
```
- Most editable parameters are in the config.py file, the model can be changed in the model.py file.
- Pipeline to label new songs with the model is given below

![alt tag](https://github.com/despoisj/DeepAudioClassification/blob/master/img/pipeline.png)
