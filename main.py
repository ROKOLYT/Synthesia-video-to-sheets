import json
import time

from downloader.downloader import download_video
from piano_detection.detect import Piano
from video_processing.processing import Video
from midi_processing.midi import Midi
 
# C4 is number 60 based on that please select the correct number for the leftmost key
# One octave is 12 keysvideo_processing

if __name__ == "__main__":
    t0 = time.time()
    # start_time = 9
    # end_time = 96
    # name = 'Fly Me To The Moon'
    # url = "https://www.youtube.com/watch?v=Wa8fAoJmjQA"
    # leftmost_key = 32
    # offset = 50
    # bpm = 120
    
    bpm = 160
    leftmost_key = 21
    start_time = 5
    end_time = 120
    url = 'https://www.youtube.com/watch?v=7R-P7ttPZEg'
    name = 'Lune M2U'
    offset = 70
    
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['bpm'] = bpm
        config['leftmost_key'] = leftmost_key
        config['offset'] = offset
        f.seek(0)
        json.dump(config, f)
    
    download_video(url, name)
    
    process_raw = Video(name, [], start_time, end_time)
    process_raw.screenshot()
    process_raw.release()
    
    print('Processing Tiles...')
    detector = Piano()
    tiles = detector.tiles()
    
    print('Processing Video...')
    process = Video(name, tiles, start_time, end_time)
    process.video()
    
    print('Processing Midi...')
    midi = Midi()
    midi.process()
    
    t1 = time.time()
    print(f"Time taken: {t1 - t0}")


