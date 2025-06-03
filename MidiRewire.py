import pretty_midi
import json

class MidiGroup():
    def __init__(self, output, inputs=[]) -> None:
        self.inputs = inputs
        self.output = output

class MidiRewire():
    def __init__(self) -> None:
        self.midi_data   = None
        self.midi_groups = {}

    def loadMidi(self, path) -> None:
        self.midi_data = pretty_midi.PrettyMIDI(path)

    def saveMidi(self, path) -> None:
        self.midi_data.write(path)

    def loadConfig(self, path) -> None:
        json_data = None
        with open(path, 'r') as file:
            json_data = json.load(file)

        for dest in json_data:
            dest_num = pretty_midi.drum_name_to_note_number(dest)
            self.midi_groups[dest_num] = MidiGroup(dest_num, json_data[dest])

    def process(self) -> None:
        # Create map that's easier to use for processing
        midi_map = {}
        for group in self.midi_groups.values():
            for input in group.inputs:
                midi_map[input] = group.output

        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                if note.pitch in list(midi_map.keys()):
                    note.pitch = int(midi_map[note.pitch])


if __name__ == "__main__":
    mr = MidiRewire()
    mr.loadConfig("./example/ezd_to_general_midi_config.json")
    mr.loadMidi("./input.mid")
    mr.process()
    mr.saveMidi("./output.mid")
