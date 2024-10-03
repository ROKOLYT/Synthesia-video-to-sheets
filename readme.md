# ⚠️🚧 Warning: Under Development 🚧⚠️

**This program is currently under development and is not in its final form. It may not work as expected in its current state. Use at your own risk.**

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
    offset = 0  # Offset to synchronize video and audio
    ```
2. Run the application:
    ```sh
    python main.py
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact [your email].