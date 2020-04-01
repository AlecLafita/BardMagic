# BardMagic
Scripts for generate keyboard inputs from a MIDI song files. Maybe is useful to autoplay as a bard on some mmo?

## Usage
- **TransformSong** script transforms all the *.mid* files located on a directory to our *.json* format.
- **BardMagic** script plays the current *.json* song file as specified

### Configuration
The scripts use the configuration at **config.json**, with the current keys:
- binds: Contains the mapping from the notes to the keyboard key. "-" stands for rest.
- sourceSongsDirectory: Local directory from the script execution where the songs to be transformed are located.
- destinySongsDirectory: Local directory from the script execution where the songs transformation will be saved.
- songToPlayFileName: Name of the *.json* file the BardMagic script will search to play.
- BPM: Beats per minute for the play 
- minimumNotesForTrack: When transforming a song, if a track have less notes than this value, it will be discarded.
- maximumOctaves: Maximum number of octaves transformed song can have.
