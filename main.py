import argparse
import os
import re
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

parser = argparse.ArgumentParser()

def url_check(url):
    """
    Checks if URL has key words to determine if it is a Youtube URL
    Returns the URL if keywords are found and a parser error if they are not found
    """
    if "youtube.com" not in url and "youtu.be" not in url:
        parser.error("Not A Youtube URL. Please try again")       
    return url

def output_check(output):
    """
    Checks if directory path exists and creates directory if it does not
    returns a parser error if the directory cannot be created
    """
    if not os.path.exists(output):
        try:
            print("Directory does not exist\nCreating Directory")
            os.mkdir(output)
        except:
            parser.error("Not a valid directory. Please try again")

    return output

def resolution_check(resolution):
     """
     Will check with regex comparison if resolution is using a valid format
     If it is not a valid resolution, it will use parser default
     """
     res_pattern = r"[0-9]?[0-9]{3}p"
     if not re.fullmatch(res_pattern, resolution):
         print("Not a valid resolution. will use default resolution")
         resolution = parser.get_default("resolution")
         
     return resolution

def video_progress(stream, data_chunk, bytes_remaining):
    """
    Calculates the percent completion of the download and prints the progress for the user
    """
    current_bytes = stream.filesize - bytes_remaining
    progress = int((current_bytes / stream.filesize) * 100)
    print(f"{progress}%")

def video_completed(stream, file_path):
    """
    prints a download completed message and the location of the downloaded file
    """
    print(f"Download completed.\nLocation: {file_path}\n")

# Adds required argument, url, and calls url_check function to ensure the url is valid
parser.add_argument(
    "url", 
    help="URL of the Youtube video. Use format: \"URL\"", 
    type=url_check
    )
# Adds optional argument, --output, and calls output_check funtion to ensure directory exists
parser.add_argument(
    "--output", 
    help="Destination directory for downloads. Use format: --url \"path\"", 
    type=output_check
    )
# Adds optional argument, --resolution, and calls resolution_check to ensure resolution is valid
parser.add_argument(
    "--resolution", 
    help="Chosen resolution for video. Use format: --resolution ###p or ####p",
    type=resolution_check
    )
# Sets default values for output and resolution if either is left blank
parser.set_defaults(output=os.path.join(os.getcwd(), "downloads"), resolution = "480p")
args = parser.parse_args()

url = args.url
output = args.output
resolution = args.resolution

try: # Searches for video based on URL and filters for resolution and files with audio and video
    yt = YouTube(url, on_progress_callback=video_progress, on_complete_callback=video_completed)
    video = yt.streams.filter(resolution=resolution, progressive=True).first()
except VideoUnavailable as e: # Raises error if URL is not a valid youtube video
    print("\nInvalid URL. Please try again with a valid URL\n")
    raise e

if video is None: # If no videos are found, it will default to getting the highest resolution
    print("\nChosen resolution not available\nDefaulting to highest resolution available")
    video = yt.streams.filter(progressive=True).get_highest_resolution()
    resolution = video.resolution

print(f"\nDownload Information:\n url: {url}\n output: {output}\n resolution: {resolution}\n")

try: # Begins downloading the video
    video.download(output_path=output)
except ConnectionAbortedError as e: # Raises an error if the download has failed or is interrupted
    print("\nConnection was interrupted while downloading the file. Please try again\n")
    raise e
except PermissionError as e: # Raises an error if the user does not have write access to the folder
    print("\n You do not have \'write\' access to the designated directory\n")
    raise e
except Exception as e: # Raises an error if any other connection issue occurs when downloading
    raise e