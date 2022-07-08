# Coverting Spotify Playlists to MP3 Downloads
Utilizing the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp) video downloader to convert any public Spotify playlist to a local MP3 file. 

This script scrapes specified Spotify playlists for track information, feeds search parameters to YouTube, then returns video links to be downloaded as MP3s by yt-dlp. The intention is to provide a permanent, automated solution, to make your favorite songs avaliable offline.

# Prerequisites
- Using a Spotify account, log into the [developer portal](https://developer.spotify.com/dashboard) and create an app. You can follow this [quickstart guide](https://developer.spotify.com/documentation/web-api/quick-start/) for further instructions. Keep note of the `Client ID` and `Client Secret`. 
- Download the [latest release](https://github.com/yt-dlp/yt-dlp/releases) of `yt-dlp.exe` and store it for use in the application installation.  
- Download the [latest release](https://ffmpeg.org/download.html) of FFmpeg. This should leave you with one folder containing `ffmpeg.exe, ffplay.exe, and ffprobe.exe`.
- Download the release of [ChromeDriver](https://chromedriver.chromium.org/downloads) that matches your systems version of Chrome for fruther use. Selenium requires ChromeDriver to operate.
- Install the python library dependencies found in [requirements.txt](/requirements.txt).

# Installation and Configuration
You can install python_to_mp3 locally via this method:

- Clone the directory to a location of your choice. Ensure all files are located within the same file directory.
- Run `main.py` to establish the necessary file directory.
- Within the folder `ytdl`, place the previously downloaded `yt-dlp.exe`.
- Within the folder `chromedriver`, place the previously downloaded `chromedriver.exe`.
- Edit the file `command.bat`:
    - In line 1, replace `#PATH TO YT-DL.EXE#` with the path to `yt-dlp.exe`.
    - In line 2, replace `#FFMPEG PATH#` with the path to the folder containing FFmpeg.
    - In line 2, replace `#OUTPUT PATH#` with the desired output location for the downloaded MP3 files. Recommended path is the `tracks` folder within the working directory.
- Open `main.py` to edit. Set the variables `CLIENT_ID` and `CLIENT_SECRET` to the ID and Secret of your Spotify API application.
- In `main.py` set the variable `URI` to the Spotify URI of the playlist you wish to download. You can learn more about Spotify URI's [here](https://community.spotify.com/t5/FAQs/What-s-a-Spotify-URI/ta-p/919201). **NOTE**: Ensure that playlist privacy is set to public otherwise an error will be thrown.

# Usage
- Once installation and configuration has been completed, insert the desired URI into the script and run it. The program will begin sourcing data from Spotify, then Youtube via Selenium, and finally download the appropriate MP3s from YouTube.
- Upon completion, you can find the downloaded tracks in the directory you specified. 

# Notes
- This time it takes to complete this process varies based on the total number and length of songs. The largest batch successfully run through the program is 500 songs, but it can go higher.
- Be aware of songs that could result in high runtime videos. For example, if your playlist includes sleep sounds, YouTube has a tendency to return 10 hour loops which will immensely bog down the program.  
