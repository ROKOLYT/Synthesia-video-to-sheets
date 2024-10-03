import cv2
import numpy as np
import os

DIRECTORY = 'piano_detection/pianos/'

class Detect:
    def __init__(self, offset):
        self.offset = offset
        self.piano_row = 0
        self.min_width = 8
        self.size = 20
        self.threshold = 0.1
        self.black = 200

    def tiles(self, photo_path):
        grayscale = self.calculate_grayscale()
        # test(grayscale)
        
        image = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
        mask = self.mask_keys(image, grayscale)
        tiles = self.find_tile_centers(mask[5])
        
        original = cv2.imread(photo_path)
        self.draw_tile_centers(original, tiles)
        original = cv2.imread(photo_path)
        
        res = []
        for tile in tiles:
            x = tile
            y = self.piano_row + self.offset
            colors = original[y, x]
            d = {'x': x, 'y': y, 'colors': colors, 'original': colors, 'pressed': False}
            res.append(d)
        
        return res
        
    def calculate_grayscale(self):
        files = os.listdir(DIRECTORY)
        grayscale = np.array([])
        
        for file in files:
            image = cv2.imread(DIRECTORY + file, cv2.IMREAD_GRAYSCALE)
            grayscale = np.append(grayscale, self.color_ratio(image))
        
        grayscale = np.mean(grayscale)
        return grayscale

    def color_ratio(self, image):
            # Check if the image is loaded
        if image is None:
            raise ValueError("Error: Could not load the image.")

        # Get the height and width of the image
        height, width = image.shape

        # Ensure the image is at least 10 rows high
        if height < self.size:
            raise ValueError("Error: The image is too small. It must be at least 10 rows high.")

        # Extract the top 10 rows
        top_x_rows = image[:self.size:]

        # Calculate the average grayscale value
        average_grayscale = np.mean(top_x_rows)
        return average_grayscale

    def find_piano(self, image, grayscale):
        global PIANO_ROW
        if image is None:
            raise ValueError("Error: Could not load the image.")
        
        height, width = image.shape
        
        lower_bound = grayscale - (grayscale * self.threshold)
        upper_bound = grayscale + (grayscale * self.threshold)
            
        row = 0
        best_row = (0, 0)
        while row + self.size < height:
            rows_x = image[row:row + self.size, :]
            
            average_grayscale = np.mean(rows_x)
            
            if average_grayscale > lower_bound and average_grayscale < upper_bound:
                if best_row[1] == 0:
                    best_row = (row, average_grayscale)
                
                curr_delta = abs(grayscale - average_grayscale)
                best_delta = abs(grayscale - best_row[1])
                
                if curr_delta < best_delta:
                    best_row = (row, average_grayscale)
            
            row += 1
            
        start = best_row[0]
        end = start + self.size
        
        self.piano_row = (start + end) // 2
        
        mask = image[start:end, :]
        
        return mask

    def mask_keys(self, image, grayscale):
        piano = self.find_piano(image, grayscale)
        
        height, width = piano.shape
        
        row = piano[5:height - 5, 5:width - 5]
        
        _, keys = cv2.threshold(row, self.black, 255, cv2.THRESH_BINARY)
        
        return keys

    def find_tile_centers(self, binary_row):
        current_color = binary_row[0]
        boundaries = []
        
        tiles = []
        width = 0
        for i in range(1, len(binary_row)):
            
            # We need to add 5 to account for the offset
            if binary_row[i] != current_color:
                if not tiles:
                    boundaries.append(i)
                    current_color = binary_row[i]
                    tiles.append(width // 2)
                    width = 0
                    continue
                
                if width <= self.min_width:
                    boundaries.append(i)
                    current_color = binary_row[i]
                    width = 0
                    continue

                tiles.append(boundaries[-1] + (width // 2) + 5)
                current_color = binary_row[i]
                boundaries.append(i)
                width = 0
                
            else:
                width += 1
                
            current_color = binary_row[i]
        
        tiles.append(boundaries[-1] + (width // 2) + 5)
        
        return tiles
        
    def draw_tile_centers(self, original, tile_centers):
        
        height, width, *args = original.shape
        
        # Draw red dots on the specified row
        for center in tile_centers:
            # Ensure the center is within image boundaries
            if 0 <= center < width:
                cv2.circle(original, (center, self.piano_row + self.offset), radius=5, color=(0, 0, 255), thickness=-1)
                
        cv2.imshow('Piano', original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    
    
