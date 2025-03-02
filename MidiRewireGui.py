import customtkinter
from MidiRewire import MidiRewire
import pretty_midi

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Midi data
        self.midi = MidiRewire()
        self.all_midi_vals_str  = [str(x) for x in range(128)]
        self.all_midi_notes_str = [pretty_midi.note_number_to_name(x) for x in range(128)]
        self.all_midi_drums_str = [pretty_midi.note_number_to_drum_name(x) for x in range(128)]

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
        self.midi_boxes = []

    def openConfigDialogEvent(self):
        file = customtkinter.filedialog.askopenfile()
        if (file is not None):
            # TODO: Create reset function that also clears the widget itself
            self.midi_boxes = []
            self.scrollable_subframes = []

            self.midi.loadConfig(file.name)
            
            prev_val = None 
            for key, val in self.midi.pitch_map.items():
                # Create new group
                if val != prev_val:
                    # TODO: Create class for remap group
                    self.scrollable_subframes.append(customtkinter.CTkFrame(self.scrollable_frame))
                    self.scrollable_subframes[-1].pack(pady=5)
                    self.scrollable_subframes[-1].left  = customtkinter.CTkFrame(self.scrollable_subframes[-1], fg_color="transparent")
                    self.scrollable_subframes[-1].right = customtkinter.CTkFrame(self.scrollable_subframes[-1], fg_color="transparent")
                    self.scrollable_subframes[-1].left.grid(row=0, column=0, padx=15, pady=10)
                    self.scrollable_subframes[-1].right.grid(row=0, column=1, padx=15, pady=10)
                    # Add right side note
                    self.midi_boxes.append(customtkinter.CTkComboBox(self.scrollable_subframes[-1].right, values=self.all_midi_notes_str))    
                    self.midi_boxes[-1].set(pretty_midi.note_number_to_drum_name(int(val)))
                    self.midi_boxes[-1].pack(pady=5)
                    prev_val = val
                
                # Add left side note
                self.midi_boxes.append(customtkinter.CTkComboBox(self.scrollable_subframes[-1].left, values=self.all_midi_notes_str))
                self.midi_boxes[-1].set(pretty_midi.note_number_to_name(int(key)))
                self.midi_boxes[-1].pack(pady=5)
            
            # Cannot edit yet --> disable input
            for box in self.midi_boxes:
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