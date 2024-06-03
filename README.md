# noindex
as an artist working with video and image processing, i strive to automate as much of the process as possible. this is the current state of my process. my goal is to consolidate everything i've done into a cohesive workflow/program that i can use and share with others. feel free to contribute in any kind, everything appreciated, copyleft and also check my other repos for other scripts/code.

## Overview
`noindex.py` is a versatile MP4 compressor designed to handle various video processing tasks, including video compression, iframe removal, baking videos, and combining videos. This script utilizes `ffmpeg` to perform its operations.

## Features
- **Compress Videos**: Compresses videos with specified width, height, scaling algorithm, codec, bitrate, scenecut threshold, and GOP.
- **Remove Iframes**: Removes iframes from the video.
- **Check Iframes**: Checks the video for iframes.
- **Bake Video**: Bakes the video.
- **Combine Videos**: Combines multiple videos into one.

## Requirements
- Python 3.x
- `ffmpeg` installed and accessible in your PATH

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```
2. Navigate to the directory:
    ```bash
    cd your-repo-name
    ```

## Usage
The script can be executed with various command-line arguments to perform different tasks. Below are the available arguments:

### Arguments
- `-i` : Enter video path for compression
- `-vw` : Enter video width
- `-vh` : Enter video height
- `-sa` : Enter scale algorithm (neighbor, gauss, lanczos, experimental)
- `-c` : Enter video codec (libx264, libxvid)
- `-b` : Enter video bitrate
- `-sc` : Enter scenecut threshold
- `-gop` : Enter video GOP
- `-noa` : Remove audio track (optional/experimental)
- `-nom` : Remove metadata (optional)
- `-noi` : Remove iframes (optional)
- `-o` : Enter output name (optional)
- `-ifr` : Enter video path to remove iframes
- `-ifrC` : Enter video path to check for iframes
- `-bake` : Enter video path for baking
- `-comb` : Enter video paths comma-separated for combining

#### Notes
noindex.py has to be in the same folder as the videos atm. The log of ffmpeg ist putted on mute, so if nothing happened, check your prompt.

### Examples
```bash
python3 noindex.py -i input.mp4 -vw 1280 -vh 720 -sa lanczos -c libx264 -b 1000 -sc 40 -gop 250 -noa -nom -o output.mp4
```
Remove Iframes
```bash
python3 noindex.py -ifr input.mp4 -o output_noifr.mp4
```
Check for Iframes
```bash
python3 noindex.py -ifrC input.mp4
```
Bake Video
```bash
python3 noindex.py -bake input.mp4
```
Combine Videos
```bash
python3 noindex.py -comb "video1.mp4,video2.mp4" -o combined.mp4
```

## Todos
- handling if certain parameters not in prompt
- input different paths than current folder (path handling)
- error handling (letting person know what went wrong with input)
- simple cut editor
- putting videos together
- different video processing methods
