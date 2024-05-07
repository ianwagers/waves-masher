class Instrument:
    def __init__(self, name, waveform="Sine", duration=0.9, note="G4"):
        self.name = name
        self.waveform = waveform
        self.duration = duration
        self.note = note

    def get_waveform(self):
        return self.waveform

    def set_waveform(self, waveform):
        self.waveform = waveform
        print(f"Waveform for {self.name} set to {waveform}")

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration
        print(f"Duration for {self.name} set to {duration}")

    def get_note(self):
        return self.note

    def set_note(self, note):
        self.note = note
        print(f"Note for {self.name} set to {note}")

    def apply_changes(self, waveform, duration, note):
        try:
            self.set_waveform(waveform)
            self.set_duration(duration)
            self.set_note(note)
            print(f"Applied changes to {self.name}: Waveform={waveform}, Duration={duration}, Note={note}")
        except Exception as e:
            print(f"Error applying changes to {self.name}: {e}", exc_info=True)