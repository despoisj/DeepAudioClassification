# -*- coding: utf-8 -*-
import eyed3

#Remove logs
eyed3.log.setLevel("ERROR")

def isMono(filename):
	audiofile = eyed3.load(filename)
	return audiofile.info.mode == 'Mono'

def getGenre(filename):
	audiofile = eyed3.load(filename)
	#No genre
	if not audiofile.tag.genre:
		return str(None)
	else:
		genere = str(audiofile.tag.genre.name.encode('utf-8'))
		genere = genere.replace('b\'', '')
		genere = genere.replace('\'', '')
		return genere




	
