#pip install music21
from music21 import *
import json

SongBaseBaseName = "song"
######################
def ObtainMinMaxOctaves(Track) :
    OctavesAppearances = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    MinOctave = 11
    MaxOctave = 0
    for NoteRest in Track.notes:
        if NoteRest.isNote:
            MinOctave = min(MinOctave, NoteRest.octave)
            MaxOctave = max(MaxOctave , NoteRest.octave)
            OctavesAppearances[NoteRest.octave] += 1
    print(OctavesAppearances)
    if (MaxOctave - MinOctave > 2) :
        print("WARNING. There are needed", MaxOctave - MinOctave + 1, "octaves, for the", Track.id, "track. Some notes will be removed lmao")
    #TODO obtain minmax octaves from appearances
    print("MinMaxOctaves:", MinOctave, MaxOctave)
    return MinOctave, MaxOctave

def GenerateTrackFile(TrackName, Track) :
    notes = []
    times = []
        
    MinOctave, MaxOctave = ObtainMinMaxOctaves(Track)
    for NoteRest in Track.notesAndRests:
        times.append(float(NoteRest.duration.quarterLength))
        if NoteRest.isRest:
            notes.append("-")
            #print("-", NoteRest.duration.quarterLength)
        elif NoteRest.isNote:
            NoteName = NoteRest.name.replace("-","b") #Transform flat nomenclature
            if NoteRest.octave < MinOctave or NoteRest.octave > MaxOctave :
                notes.append("-")
            if NoteRest.octave == MinOctave :
                notes.append("d" + NoteName)
            elif NoteRest.octave == MaxOctave :
                notes.append("u" + NoteName)
            else :
                notes.append(NoteName)                
            #print(NoteRest.name, NoteRest.duration.quarterLength,NoteRest.duration.type, NoteRest.octave)

    ResultJSON = {"notes" : notes, "times": times}
    with open(SongBaseBaseName + TrackName + ".json", "w") as JSONFile:
        JSONFile.write(json.dumps(ResultJSON))

def TransformSong(FileName):
    SongName = FileName.replace(".mid","")
    Score = converter.parse(FileName)
    for Index, Track in enumerate(Score.parts) :
       GenerateTrackFile(SongName + "Track" + str(Index), Track)

######################
TransformSong('ventus.mid')
#TODO trasnform all files from a directory

print("Files converted!")