import argparse
import os
import re
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

parser = argparse.ArgumentParser()

def url_check(url):
    # Checks if URL has key words to determine if it is a Youtube URL
    if "youtube.com" not in url and "youtu.be" not in url:
         parser.error("Not A Youtube URL. Please try again")       
    return url

def output_check(output):
    # Checks if directory path exists and creats directory if it does not
    if not os.path.exists(output):
        try:
            print("Directory does not exist\nCreating Directory")
            os.mkdir(output)
        except:
            parser.error("Not a valid directory. Please try again")
    
    return output

def resolution_check(resolution):
     # Will check if resolution is a valid resolution
     res_pattern = r"[0-9]?[0-9]{3}p"
     if not re.fullmatch(res_pattern, resolution):
         resolution = "720p"
         print("Not a valid resolution. Please try again")
     return resolution

def video_progress(stream, data_chunk, bytes_remaining):
    current_bytes = stream.filesize - bytes_remaining
    progress = int((current_bytes / stream.filesize) * 100)
    print(f"{progress}%")

def video_completed(stream, file_path):
    print("Download completed.\nLocation:", file_path)

parser.add_argument(
    "url", 
    help="URL of the Youtube video. Use format: \"URL\"", 
    type=url_check
    )
parser.add_argument(
    "--output", 
    help="Destination directory for downloads. Use format: --url \"path\"", 
    type=output_check
    )
parser.add_argument(
    "--resolution", 
    help="Chosen resolution for video. Use format: --resolution ###p or ####p",
    type=resolution_check
    )
parser.set_defaults(output=os.path.join(os.getcwd(), "downloads"), resolution = "720p")
args = parser.parse_args()

url = args.url
output = args.output
resolution = args.resolution

try:
    yt = YouTube(url, on_progress_callback=video_progress, on_complete_callback=video_completed)
    video = yt.streams.filter(resolution=resolution, progressive=True).first()
except VideoUnavailable as e:
    print("\nInvalid URL. Please try again with a valid URL\n")
    raise e

if video is None:
    print("Chosen resolution not available\nDefaulting to highest available")
    video = yt.streams.filter(progressive=True).get_highest_resolution()
    resolution = video.resolution

print(f"\nDownload Information:\n url: {url}\n output: {output}\n resolution: {resolution}\n")

try:
    video.download(output_path=output)
except:
    raise Exception("Download has failed. Please try again")