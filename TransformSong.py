#pip install music21
from music21 import *
import json
import os

MaximumOctaves = 3

######################
def ParseConfig() :
    global SongBaseBaseName
    global SourceSongsLocalDirectory
    global GeneratedSongsLocalDirectory
    global MinimumNotes
    global MaximumOctaves

    with open('config.json') as JSONFile:
        JSONConfig = json.load(JSONFile)
        SongBaseBaseName = JSONConfig["songToPlayFileName"]
        SourceSongsLocalDirectory = JSONConfig["sourceSongsDirectory"]
        GeneratedSongsLocalDirectory = JSONConfig["destinySongsDirectory"]
        MinimumNotes = JSONConfig["minimumNotesForTrack"]
        MaximumOctaves = JSONConfig["maximumOctaves"]

def TransformChordsToNotes(Pitches) :
    NotesAndRests= []
    for Pitch in Pitches :
        if Pitch.isChord :
            NotesAndRests.append(Pitch.notes[0]) #TODO maybe take the lower one?
        else :
            NotesAndRests.append(Pitch)
    return NotesAndRests

def CalculateBiggestSubHistogramStart(Histogram, SubHistogramSize) :
    BiggestSubHistogramStart = 0
    BiggestSubHistogramSum = 0

    for SubHistogramStart in range(0, len(Histogram)- SubHistogramSize) :
        SubHistogramSum = sum(Histogram[SubHistogramStart:(SubHistogramStart + SubHistogramSize)])
        if (SubHistogramSum > BiggestSubHistogramSum) :
            BiggestSubHistogramSum = SubHistogramSum
            BiggestSubHistogramStart = SubHistogramStart

    return BiggestSubHistogramStart

def ObtainMinMaxOctaves(Pitches) :
    OctavesAppearances = []
    NumOctaves = 10
    for Octave in range(0, NumOctaves  + 1) :
        OctavesAppearances.append(0)
    MinOctave = NumOctaves + 1
    MaxOctave = 0

    for Pitch in Pitches:
        if Pitch.isNote:
            MinOctave = min(MinOctave, Pitch.octave)
            MaxOctave = max(MaxOctave , Pitch.octave)
            OctavesAppearances[Pitch.octave] += 1

    NeededOctaves = MaxOctave - MinOctave + 1
    if NeededOctaves > MaximumOctaves :
        MinOctave = CalculateBiggestSubHistogramStart(OctavesAppearances, MaximumOctaves)
        MaxOctave = MinOctave + MaximumOctaves - 1
        RemovesNotes = sum(OctavesAppearances) - sum(OctavesAppearances[MinOctave:(MaxOctave + 1)])
        print("WARNING. There are needed", NeededOctaves, "octaves, and we only can have", MaximumOctaves, "so", RemovesNotes, "notes will be removed lmao")

    return MinOctave, MaxOctave

def GenerateTrackFile(TrackName, Track) :
    print("Converting " + SongBaseBaseName + TrackName  + "...")
    notes = []
    times = []

    TrackPitches = TransformChordsToNotes(Track.notesAndRests)        
    MinOctave, MaxOctave = ObtainMinMaxOctaves(TrackPitches)
    for Pitch in TrackPitches :       
        if Pitch.isRest:
            times.append(float(Pitch.duration.quarterLength))
            notes.append("-")
        elif Pitch.isNote and Pitch.octave >= MinOctave and Pitch.octave <= MaxOctave :
            times.append(float(Pitch.duration.quarterLength))
            NoteName = Pitch.name.replace("-","b") #Transform flat nomenclature
            if Pitch.octave == MinOctave :
                NoteName = "d" + NoteName
            elif Pitch.octave == MaxOctave :
                NoteName = "u" + NoteName
            notes.append(NoteName)

    if len(notes) >= MinimumNotes :
        ResultJSON = {"notes" : notes, "times": times}
        with open(GeneratedSongsLocalDirectory + "/" + SongBaseBaseName + TrackName + ".json", "w") as JSONFile:
            JSONFile.write(json.dumps(ResultJSON))
        print("Converted " + SongBaseBaseName + TrackName  + "!")
    else : 
        print(SongBaseBaseName + TrackName  + "couldn't be converted, it just have", len(notes), "notes!")

def TransformSong(FileName):
    SongName = FileName.replace(".mid","").replace(SourceSongsLocalDirectory + "/", "")
    Score = converter.parse(FileName)
    Index = 0
    for Track in Score.parts :
        if len(Track.notesAndRests) > 1 :
            GenerateTrackFile(SongName + "Track" + str(Index), Track)
            Index += 1
        else : 
            for Element in Track.voices: 
                GenerateTrackFile(SongName + "Track" + str(Index), Element)
                Index += 1

######################
ParseConfig()
if not os.path.exists(GeneratedSongsLocalDirectory):
    os.mkdir(GeneratedSongsLocalDirectory)

for Song in os.listdir(SourceSongsLocalDirectory):
    if Song.find(".mid") != -1:
        TransformSong(SourceSongsLocalDirectory + '/' + Song)
print("Files converted!")