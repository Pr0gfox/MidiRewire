# MidiRewire

Python app that can remap MIDI notes in files.

> Hey, I made this smol app because apps that we use for our band have different MIDI mappings and this tool helps the conversion process.

# Requirements

* Python
* Pip

# Getting started

After cloning this repository, install dependencies

```sh
pip install -r ./requirements.txt
```

Then, you should be able to run the app.

```sh
python MidiRewireGui.py  # For the GUI version
python MidiRewire.py     # For the CONSOLE version
```

> **NOTE:** The console app has some hardcoded relative paths in its `__name__ == "__main__"` section. Feel free to change that to suit your needs. Later, the paths will be passed down as console arguments.

# Usage

To convert MIDI files, you must load the MIDI file to convert and load the configuration file you want to use for the conversion. Upon successful config load, a MidiRewire map will appear in the app depicting the notes that the app will look for and how it will change them. 

> **NOTE:** In the future, config files will be editable from the app, but for now, it is read-only. 

![GUI application](/doc/gui_app.png)

## Config file

The config file defines the note mappings. The key is the note that you would like to map **TO** and the value contains one or multiple notes that you would like to map **FROM**. Config must contain MIDI **values** (not names). See the [example configuration](./example/config.json) to get an idea how it should look like.

---

***Have fun!***
