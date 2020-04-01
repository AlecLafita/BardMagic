#pip install music21
from music21 import *
import json

SongBaseBaseName = "song"
SourceSongsLocalDirectory = "songs"
GeneratedSongsLocalDirectory = "generatedSongs"
######################

def TransformChordsToNotes(Pitches) :
    NotesAndRests= []
    for Pitch in Pitches :
        if Pitch.isChord :
            print("CHORD", Pitch.notes)
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
    print(OctavesAppearances)
    if (MaxOctave - MinOctave > 2) :
        print("WARNING. There are needed", MaxOctave - MinOctave + 1, "octaves, for the", Track.id, "track. Some notes will be removed lmao")
    #TODO obtain minmax octaves from appearances
    print("MinMaxOctaves:", MinOctave, MaxOctave)
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
            #print("-", Pitch.duration.quarterLength)
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
            #print(Pitch.name, Pitch.duration.quarterLength,Pitch.duration.type, Pitch.octave)
        else :
            raise ValueError("Parsing undefined pitch")
    ResultJSON = {"notes" : notes, "times": times}
    with open(GeneratedSongsLocalDirectory + "/" +SongBaseBaseName + TrackName + ".json", "w") as JSONFile:
        JSONFile.write(json.dumps(ResultJSON))

def TransformSong(FileName):
    SongName = FileName.replace(".mid","").replace(SourceSongsLocalDirectory + "/", "")
    Score = converter.parse(FileName)
    for Index, Track in enumerate(Score.parts) :
       GenerateTrackFile(SongName + "Track" + str(Index), Track)

######################
TransformSong(SourceSongsLocalDirectory + '/' + 'dragonrostisland.mid')
#TODO trasnform all files from a directory

print("Files converted!")