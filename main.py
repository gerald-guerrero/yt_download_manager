import argparse
import os
import re

parser = argparse.ArgumentParser()

def url_check(url):
    # Checks if URL has key words to determine if it is a Youtube URL
    if "youtube.com" not in url:
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
         print("Not a valid resolution. Defaulting to 720p")
     return resolution


parser.add_argument("url", help="URL of the Youtube video you want to download", type=url_check)
parser.add_argument("--output", help="Destination directory for the video", type=output_check)
parser.add_argument("--resolution", help="Chosen resolution for video", type=resolution_check)
parser.set_defaults(output=os.path.join(os.getcwd(), "downloads"), resolution = "720p")
args = parser.parse_args()

url = args.url
output = args.output
resolution = args.resolution

print("You selected:", url, output, resolution)