# Piano Video to Sheets

This project converts piano performance videos into sheet music.

## Features

- **Video Analysis**: Extracts piano key presses from video.
- **Sheet Music Generation**: Converts extracted data into readable sheet music.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/piano_video_to_sheets.git
    ```
2. Navigate to the project directory:
    ```sh
    cd piano_video_to_sheets
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Set the parameters in the script according to your video (example values provided):
    ```python
    bpm = 120  # Beats per minute of the piece
    leftmost_key = 21  # MIDI number of the leftmost key on the piano
    start_time = 0  # Start time of the transcription in seconds
    end_time = 60  # End time of the transcription in seconds
    url = 'https://www.example.com'  # URL of the video
    name = 'Example Piece'  # Name of the piece
    offset = 0  # Offset to line up they key detection
    ```
2. Run the application:
    ```sh
    python main.py
    ```

## Leftmost Key

The leftmost key can be identified by counting the keys to the left of C4. The C4 key corresponds to `key = 60`. In the future, I may implement logic to automatically determine the leftmost key. If you are interested in contributing, feel free to submit a pull request.

## Offset

Adjust the offset until the red dots align with both the black and white keys. **Ensure the red dots are not positioned at the very top of the keys, as some videos may have light effects in that area.**

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue.
