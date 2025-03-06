import customtkinter
import MidiRewire
import pretty_midi

ALL_MIDI_VALS_STR  = [str(x) for x in range(128)]
ALL_MIDI_NAMES_STR = [pretty_midi.note_number_to_name(x) for x in range(128)]
ALL_MIDI_DRUMS_STR = [pretty_midi.note_number_to_drum_name(x) for x in range(128)]

class MidiGroupGui(MidiRewire.MidiGroup):
    def __init__(self, parent, midi_group) -> None:
        super().__init__(midi_group.output, midi_group.inputs)
        self.parent      = parent
        self.frame       = customtkinter.CTkFrame(parent)
        self.left_frame  = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.right_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.frame.pack(pady=5)
        self.left_frame.grid(row=0, column=0, padx=15, pady=10)
        self.right_frame.grid(row=0, column=1, padx=15, pady=10)
        self.input_boxes = {}
        for input in self.inputs:
            self.__addInputBox(input)
        self.output_box = customtkinter.CTkComboBox(self.right_frame, values=ALL_MIDI_DRUMS_STR)
        self.output_box.set(pretty_midi.note_number_to_drum_name(int(self.output)))
        self.output_box.pack()

    def addInput(self, input) -> None:
        self.inputs.append(input)
        self.__addInputBox(input)

    def __addInputBox(self, input) -> None:
        self.input_boxes[input] = customtkinter.CTkComboBox(self.left_frame, values=ALL_MIDI_NAMES_STR)
        self.input_boxes[input].set(pretty_midi.note_number_to_name(int(input)))
        self.input_boxes[input].pack(pady=5)

    def removeInput(self, input) -> None:
        self.input_boxes[input].destroy()
        del self.input_boxes[input]
        self.inputs.remove(input)

    def destroy(self):
        self.frame.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Midi data
        self.midi = MidiRewire.MidiRewire()

        # Configure window
        self.title("MidiRewire")
        self.geometry(f"{640}x{480}")

        # Configure layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0), weight=1)

        # Create sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar, text="MidiRewire", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.load_midi_button = customtkinter.CTkButton(self.sidebar, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.openMidiDialogEvent, text="Load MIDI")
        self.load_midi_button.grid(row=1, column=0, padx=20, pady=10)
        self.load_config_button = customtkinter.CTkButton(self.sidebar, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.openConfigDialogEvent, text="Load config")
        self.load_config_button.grid(row=2, column=0, padx=20, pady=10)
        self.export_midi_button = customtkinter.CTkButton(self.sidebar, command=self.exportMidiDialogEvent, text="Export MIDI")
        self.export_midi_button.grid(row=3, column=0, padx=20, pady=10)

        # Create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Before --> After    ", fg_color="transparent", label_font=customtkinter.CTkFont(size=16, weight="bold"))
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def openConfigDialogEvent(self):
        file = customtkinter.filedialog.askopenfile()
        if (file is not None):
            # Load config and convert items
            self.midi.loadConfig(file.name)
            for group in self.midi.midi_groups.values():
                self.midi.midi_groups[group.output] = MidiGroupGui(self.scrollable_frame, group)

            # Cannot edit yet --> disable input
            for group in self.midi.midi_groups.values():
                group.output_box.configure(state="readonly")
                group.output_box.configure(values=[])
                for box in group.input_boxes.values():
                    box.configure(state="readonly")
                    box.configure(values=[])

            print("Config loaded:", file.name)

    def openMidiDialogEvent(self):
        file = customtkinter.filedialog.askopenfile()
        if (file is not None):
            self.midi.loadMidi(file.name)
            print("MIDI loaded:", file.name)

    def exportMidiDialogEvent(self):
        file = customtkinter.filedialog.asksaveasfile()
        if (file is not None):
            self.midi.process()
            self.midi.saveMidi(file.name)
            print("MIDI exported: ", file.name)


if __name__ == "__main__":
    app = App()
    app.mainloop()