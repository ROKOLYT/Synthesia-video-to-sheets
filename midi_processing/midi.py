from midiutil import MIDIFile
import json


class Midi:
    def __init__(self):
        # Load data from JSON file
        with open('config.json') as f:
            config = json.load(f)
            self.left_most_key = config['leftmost_key']
            self.bpm = config['bpm']
            self.tile_path = config['tiles_path']
            self.output_dir = config['output_path']
        
        with open(self.tile_path) as f:
            self.data = json.load(f)

        self.tiles = self.data['tiles']
        self.fps = self.data['FPS']  # Get the frames per second from your data
        self.track = 0
        self.channel = 0

        # Create a MIDI file with one track
        self.MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track automatically created)
        self.MyMIDI.addTempo(self.track, 0, self.bpm)  # Start tempo at time 0
        
    # Function to convert seconds to beats
    def seconds_to_beats(self, seconds, bpm):
        bts = bpm / 60
        return seconds * bts

    def process(self):
        self.validate_tiles()

        # Go through each tile and add corresponding MIDI notes
        for idx, tile in enumerate(self.tiles):
            if not tile:
                continue
            self.process_tiles(idx, tile)
        
        self.save_midi()
        
    def validate_tiles(self):
        for idx, tile in enumerate(self.tiles):
            length = len(tile)
            if length % 2 != 0:
                print(f"Tile {idx + self.left_most_key} has an odd number of frames. Ignoring the last frame. starts at {tile[0]}")
                
    def save_midi(self):
        output_file = f"{self.output_dir}/{self.data['name']}.mid"
        # Write the MIDI file
        with open(output_file, "wb") as output_file:
            self.MyMIDI.writeFile(output_file)

        print(f"MIDI file created and saved as {self.data['name']}.mid")
        
    
    def process_tiles(self, idx, tile):
        for i in range(0, len(tile), 2):
            try:
                # Ensure we have a pair of start and end frames
                start_frame = tile[i]
                end_frame = tile[i + 1]
            except IndexError:
                continue
            
            # Convert frame numbers to seconds
            start_time_sec = start_frame / self.fps
            end_time_sec = end_frame / self.fps
            
            # Convert start and end times to beats
            start_beats = self.seconds_to_beats(start_time_sec, self.bpm)
            end_beats = self.seconds_to_beats(end_time_sec, self.bpm)
            
            # Calculate the duration in beats
            duration = end_beats - start_beats
            
            # Add the note for the specified duration
            pitch = idx + self.left_most_key  # Map tile index to MIDI pitch (adjust as necessary)
            
            # Add the note to the MIDI track
            self.MyMIDI.addNote(self.track, self.channel, pitch, start_beats, duration, 100)
