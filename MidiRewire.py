import pretty_midi
import json

class MidiRewire():
    def __init__(self) -> None:
        self.midi_data = None
        self.pitch_map = {}

    def loadMidi(self, path) -> None:
        self.midi_data = pretty_midi.PrettyMIDI(path)

    def saveMidi(self, path) -> None:
        self.midi_data.write(path)

    def loadConfig(self, path) -> None:
        json_data = None
        with open(path, 'r') as file:
            json_data = json.load(file)

        for dest in json_data:
            for source in json_data[dest]:
                self.pitch_map[source]=dest

    def process(self) -> None:
        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                if note.pitch in list(self.pitch_map.keys()):
                    note.pitch = int(self.pitch_map[note.pitch])


if __name__ == "__main__":
    mr = MidiRewire()
    mr.loadConfig("./example/config.json")
    mr.loadMidi("./input.mid")
    mr.process()
    mr.saveMidi("./output.mid")
