#pip install pynput
import json
import time
from pynput.keyboard import Controller

######################
def ParseConfig():
    with open('config.json') as JSONFile:
        return json.load(JSONFile)

def SongConfig() : 
    with open('song.json') as JSONFile:
        JSON = json.load(JSONFile)
        return JSON["notes"], JSON["times"]

current_time = lambda: int(round(time.time()))

######################
BindingConfig = ParseConfig()
Notes, Times = SongConfig()

keyboard = Controller()

tempo = 60/120
CurrentNoteIndex = 0

time.sleep(2)
keyboard.press('1')
keyboard.release('1')
time.sleep(2)

while CurrentNoteIndex < len(Notes) :
	if CurrentNoteIndex > 0 :
		keyboard.release(BindingConfig[Notes[CurrentNoteIndex - 1]])
	keyboard.press(BindingConfig[Notes[CurrentNoteIndex]])
	time.sleep(tempo*Times[CurrentNoteIndex])
	CurrentNoteIndex += 1