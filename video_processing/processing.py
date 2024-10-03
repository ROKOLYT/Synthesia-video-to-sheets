import cv2
import numpy as np
import json

DIRECTORY = "G:/.Programs/piano_video_to_sheets/videos/"
OUT_DIR = "G:/.Programs/piano_video_to_sheets/output.json"
SCREENSHOT = 'G:/.Programs/piano_video_to_sheets/piano_detection/tiles.jpg'

class Process:
    def __init__(self, name, tiles, start_time, end_time):
        self.diff = 50
        self.diff_original = 20
        self.video_path = DIRECTORY + name + '.mp4'
        self.cap = cv2.VideoCapture(self.video_path)
        self.tiles = tiles
        self.fps = round(self.cap.get(cv2.CAP_PROP_FPS))
        self.frames = int(end_time * self.fps)
        self.frame_size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.target_frame = start_time * self.fps
        self.first_iter = True
        self.data = {'FPS': self.fps, 'name': name, 'tiles': [[] for _ in range(len(tiles))]}

        # Create a VideoWriter object to save the output video
        self.output_video_path = DIRECTORY + name + '_output.mp4'
        self.out = cv2.VideoWriter(self.output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, self.frame_size)

        # Initialize with a list where each entry corresponds to the last frame a circle was drawn for each tile
        self.circle_tiles = [False] * len(self.tiles)
        
        if not self.cap.isOpened():
            raise ValueError("Error: Could not open the video.")
        
    def frame(self):
        ret, frame = self.cap.read()
        
        if self.first_iter:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.target_frame)
            self.first_iter = False
        
        if not ret:
            raise ValueError("Error: Could not read the frame.")
        
        for idx, tile in enumerate(self.tiles):
            x = tile['x']
            y = tile['y']
            pressed = tile['pressed']
            
            # Get current and original colors
            (b, g, r) = frame[y, x]
            (bo, go, ro) = tile['colors']
            (bd, gd, rd) = tile['original']
            
            # Convert to int32 to avoid overflow
            b, g, r = np.array(b, dtype=np.int32), np.array(g, dtype=np.int32), np.array(r, dtype=np.int32)
            bo, go, ro = np.array(bo, dtype=np.int32), np.array(go, dtype=np.int32), np.array(ro, dtype=np.int32)
            bd, gd, rd = np.array(bd, dtype=np.int32), np.array(gd, dtype=np.int32), np.array(rd, dtype=np.int32)
            
            dif_sum = abs(b - bo) + abs(g - go) + abs(r - ro)
            diff_original = abs(b - bd) + abs(g - gd) + abs(r - rd)
            
            # If color change is detected
            if dif_sum > self.diff and diff_original > self.diff_original and not pressed:
                self.circle_tiles[idx] = True
                self.data['tiles'][idx].append(self.target_frame)
                self.tiles[idx]['pressed'] = True
            
            elif diff_original < self.diff_original and pressed:
                if self.circle_tiles[idx]:
                    self.data['tiles'][idx].append(self.target_frame)
                self.circle_tiles[idx] = False
                self.tiles[idx]['pressed'] = False
                
            tile['colors'] = (b, g, r)
        
        frame = self.circles(frame)

        # Write the modified frame to the output video
        self.out.write(frame)
        self.target_frame += 1
        
    def video(self):
        self.non_piano_frames()
        
        while self.target_frame <= self.frames:
            try:
                self.frame()
            except ValueError:
                break
        
        # Release the video writer and capture objects
        self.cap.release()
        self.out.release()
        with open(OUT_DIR, 'w') as f:
            json.dump(self.data, f, indent=4)
        
    def circles(self, frame):
        for idx, draw_tile in enumerate(self.circle_tiles):
            if not draw_tile:
                continue
            tile = self.tiles[idx]
            x = tile['x']
            y = tile['y']
            
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
        
        return frame
        
    def non_piano_frames(self):
        for i in range(self.target_frame):
            ret, frame = self.cap.read()
            self.out.write(frame)
        
    def screenshot(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.target_frame)
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Error: Could not read the frame.")
        
        cv2.imwrite(SCREENSHOT, frame)
    
    def release(self):
        self.cap.release()
        self.out.release()