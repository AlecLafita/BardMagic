#pip install music21
from music21 import *
import json
import os

######################
def ParseConfig() :
    global SongBaseBaseName
    global SourceSongsLocalDirectory
    global GeneratedSongsLocalDirectory

    with open('config.json') as JSONFile:
        JSONConfig = json.load(JSONFile)
        SongBaseBaseName = JSONConfig["sourceSongsDirectory"]
        SourceSongsLocalDirectory = JSONConfig["sourceSongsDirectory"]
        GeneratedSongsLocalDirectory = JSONConfig["destinySongsDirectory"]

def TransformChordsToNotes(Pitches) :
    NotesAndRests= []
    for Pitch in Pitches :
        if Pitch.isChord :
            NotesAndRests.append(Pitch.notes[0]) #TODO maybe take the lower one?
        else :
            NotesAndRests.append(Pitch)
    return NotesAndRests

def ObtainMinMaxOctaves(Pitches) :
    OctavesAppearances = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    MinOctave = 11
    MaxOctave = 0
    for Pitch in Pitches:
        if Pitch.isNote:
            MinOctave = min(MinOctave, Pitch.octave)
            MaxOctave = max(MaxOctave , Pitch.octave)
            OctavesAppearances[Pitch.octave] += 1
    if (MaxOctave - MinOctave > 2) :
        print("WARNING. There are needed", MaxOctave - MinOctave + 1, "octaves. Some notes will be removed lmao")
    #TODO obtain minmax octaves from appearances
    return MinOctave, MaxOctave

def GenerateTrackFile(TrackName, Track) :
    notes = []
    times = []

    TrackPitches = TransformChordsToNotes(Track.notesAndRests)        
    MinOctave, MaxOctave = ObtainMinMaxOctaves(TrackPitches)
    for Pitch in TrackPitches :
        times.append(float(Pitch.duration.quarterLength))
        if Pitch.isRest:
            notes.append("-")
        elif Pitch.isNote:
            NoteName = Pitch.name.replace("-","b") #Transform flat nomenclature
            if Pitch.octave < MinOctave or Pitch.octave > MaxOctave :
                notes.append("-")
            if Pitch.octave == MinOctave :
                notes.append("d" + NoteName)
            elif Pitch.octave == MaxOctave :
                notes.append("u" + NoteName)
            else :
                notes.append(NoteName)                
        else :
            raise ValueError("Parsing undefined pitch")

    if len(notes) > 0 :
        ResultJSON = {"notes" : notes, "times": times}
        with open(GeneratedSongsLocalDirectory + "/" + SongBaseBaseName + TrackName + ".json", "w") as JSONFile:
            JSONFile.write(json.dumps(ResultJSON))
        print("Converted " + SongBaseBaseName + TrackName  + "!")

def TransformSong(FileName):
    SongName = FileName.replace(".mid","").replace(SourceSongsLocalDirectory + "/", "")
    Score = converter.parse(FileName)
    for Index, Track in enumerate(Score.parts) :
       GenerateTrackFile(SongName + "Track" + str(Index), Track)

######################
ParseConfig()
if not os.path.exists(GeneratedSongsLocalDirectory):
    os.mkdir(GeneratedSongsLocalDirectory)

for Song in os.listdir(SourceSongsLocalDirectory):
    if Song.find(".mid") != -1:
        TransformSong(SourceSongsLocalDirectory + '/' + Song)
print("Files converted!")