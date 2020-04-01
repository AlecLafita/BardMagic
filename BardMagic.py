#pip install pynput
import json
import time
from pynput.keyboard import Controller

######################
def ParseConfig():
	with open('config.json') as JSONFile :
		JSON = json.load(JSONFile)
		return JSON["binds"], JSON["BMP"]

def SongConfig() : 
	with open('config.json') as JSONFile:
		SongFileName =  json.load(JSONFile)["songToPlayFileName"]
		with open(SongFileName + '.json') as JSONFile:
			JSON = json.load(JSONFile)
			return JSON["notes"], JSON["times"]

current_time = lambda: int(round(time.time()))

######################
BindingConfig, BMP = ParseConfig()
Notes, Times = SongConfig()

Keyboard = Controller()

Tempo = 60/BMP
CurrentNoteIndex = 0

time.sleep(2)
Keyboard.press('1')
Keyboard.release('1')
time.sleep(1)

while CurrentNoteIndex < len(Notes) :
	if CurrentNoteIndex > 0 :
		Keyboard.release(BindingConfig[Notes[CurrentNoteIndex - 1]])
	Keyboard.press(BindingConfig[Notes[CurrentNoteIndex]])
	time.sleep(Tempo * Times[CurrentNoteIndex])
	CurrentNoteIndex += 1