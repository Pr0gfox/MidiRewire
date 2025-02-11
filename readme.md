# MidiRewire

Python app that can remap MIDI notes in files.

Hey, I made this smol app because apps that we use for our band have different MIDI mappings and this tool helps the conversion process.
This is the proof of concept stage, but maybe you will find it useful anyway.

# Usage

The config file defines the note mappings. The key is the note that you would like to map TO and the value contains one or more notes that you would like to map FROM. Kinda confusing at first, but you can check out the provided example config that converts a highlevel MIDI map to a simple one. That's why there are tons of input notes that map to the same output note.

Good luck!
