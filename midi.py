from midiutil import MIDIFile
import json

DIR = "G:/.Programs/piano_video_to_sheets/output.json"

# Function to convert seconds to beats
def seconds_to_beats(seconds, bpm):
    bts = bpm / 60
    return seconds * bts

def process_midi(leftmost_key, bpm):
    
    # Load data from JSON file
    with open(DIR) as f:
        data = json.load(f)

    tiles = data['tiles']
    FPS = data['FPS']  # Get the frames per second from your data
    track = 0
    channel = 0
    tempo = bpm  # In BPM

    # Create a MIDI file with one track
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track automatically created)
    MyMIDI.addTempo(track, 0, tempo)  # Start tempo at time 0
    
    for idx, tile in enumerate(tiles):
        length = len(tile)
        if length % 2 != 0:
            print(f"Tile {idx + leftmost_key} has an odd number of frames. Ignoring the last frame. starts at {tile[0]}")

    # Go through each tile and add corresponding MIDI notes
    for idx, tile in enumerate(tiles):
        if not tile:
            continue
        for i in range(0, len(tile), 2):
            try:
                # Ensure we have a pair of start and end frames
                start_frame = tile[i]
                end_frame = tile[i + 1]
            except IndexError:
                continue
            
            # Convert frame numbers to seconds
            start_time_sec = start_frame / FPS
            end_time_sec = end_frame / FPS
            
            # Convert start and end times to beats
            start_beats = seconds_to_beats(start_time_sec, tempo)
            end_beats = seconds_to_beats(end_time_sec, tempo)
            
            # Calculate the duration in beats
            duration = end_beats - start_beats
            
            # Add the note for the specified duration
            pitch = idx + leftmost_key  # Map tile index to MIDI pitch (adjust as necessary)
            
            # Add the note to the MIDI track
            MyMIDI.addNote(track, channel, pitch, start_beats, duration, 100)

    # Write the MIDI file
    with open(f"{data['name']}.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

    print(f"MIDI file created and saved as {data['name']}.mid")
