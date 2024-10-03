import time
from downloader import download_video

    
from piano_detection.detect import Detect
from video_processing.processing import Process
from midi import process_midi

SCREENSHOT = 'piano_detection/tiles.jpg'
 
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
    
    download_video(url, name)
    
    process_raw = Process(name, [], start_time, end_time)
    process_raw.screenshot()
    process_raw.release()
    
    print('Processing Tiles...')
    detector = Detect(offset)
    tiles = detector.tiles(SCREENSHOT)
    
    print('Processing Video...')
    process = Process(name, tiles, start_time, end_time)
    process.video()
    
    print('Processing Midi...')
    midi_processor = process_midi(leftmost_key, bpm)
    
    t1 = time.time()
    print(f"Time taken: {t1 - t0}")


