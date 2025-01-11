import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of the Youtube video you want to download")
parser.add_argument("--output", help="Destination directory for the video")
parser.add_argument("--resolution", help="Chosen resolution for video")
args = parser.parse_args()

url = args.url
output = args.output
resolution = args.resolution

print("You selected:", url, output, resolution)