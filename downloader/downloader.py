import yt_dlp as youtube_dl
import json

with open('config.json') as f:
    config = json.load(f)
    DIRECTORY = config['temp_path']

def download_video(url, name):
    ydl_opts = {
        'outtmpl': DIRECTORY + name + '.mp4',
        'format': 'bestvideo',
        'merge_output_format': 'mp4'
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
if __name__ == "__main__":
    download_video("https://www.youtube.com/watch?v=Qskm9MTz2V4", 'RushE')