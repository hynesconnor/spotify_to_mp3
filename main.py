# imports
import os
import re
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By

# constants
CLIENT_ID = ''
CLIENT_SECRET = ''
CWD = os.getcwd()
PATH_EXTENSION = CWD + '\\chromedriver\\1.43.0_0.crx'
PATH_DRIVER = CWD + '\\chromedriver\\chromedriver'
PATH_CSV = CWD + '\\data\\playlist_tracks.csv'
PATH_LINKS = CWD + '\\ytdl\\songlink.txt'
PATH_BAT = CWD + '\\command.bat'

URI = '' #adjust based on desired playlist

def create_dir():
    if not os.path.exists(CWD + '\\data'): # chromedriver, data, tracks, ytdl
        cur_dir = CWD + '\\'
        main_dirs = ['chromedriver', 'data', 'tracks', 'ytdl']
        for i in main_dirs:
            os.makedirs(cur_dir + i)

# connects to spotify api using credentials
# returns: api connection object
def api_connect():
    spotify = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET))
    return spotify

# using URI, grabs information of all songs in playlist
# returns dataframe of all songs in playlist
def get_tracks(spotify):
    results = spotify.playlist_tracks(URI)
    songs = results['items']
    while results['next']:
        results = spotify.next(results)
        songs.extend(results['items'])
    return songs

# selects track and artist name for each track
# returns two lists, one of track name, one of artist name
def parse_tracks(songs):
    tracks = list()
    artists = list()
    for song in songs:
        tracks.append(song['track']['name'])
        artists.append(song['track']['artists'][0]['name'])
    return tracks, artists

# writes csv file of dataframe containing track/artist information
def write_df(tracks, artists):
    df = pd.DataFrame(
        {
            'track': tracks,
            'artist': artists
        }
    )
    df.to_csv(PATH_CSV)
    print('csv written.')

# concats track and artist for searches
# returns: list of search queries
def concat_search():
    song_df = pd.read_csv(PATH_CSV, na_filter = False)
    titles = song_df['track']
    artists = song_df['artist']
    search_params = []
    for i in range(0, len(titles)):
        concat = titles[i] + ' ' + artists[i] + ' audio'
        search_params.append(concat)
    return(search_params)

# establishes selenium webdriver using chromedriver
# returns: webdriver
def webdriver_init():
    chrome_options = webdriver.ChromeOptions() # remove to test
    chrome_options.add_extension(PATH_EXTENSION)
    driver = webdriver.Chrome(executable_path = PATH_DRIVER, options = chrome_options)
    driver.implicitly_wait(5)
    return driver

# automation of youtube searches. for each search term, gets unique URL
# returns: list of video URLS
def query_links(driver, search_params):
    links = []
    count = 1
    for query in search_params:
        print(count, '/', len(search_params)) #video-title div#contents ytd-item-section-renderer>div#contents a#thumbnail
        print(query)
        query = re.sub('[!@#$%]', '', query) # ugly, sanitize special characters
        driver.get('https://www.youtube.com/results?search_query={}'.format(query))
        web_element = driver.find_element(By.CSS_SELECTOR, 'div#contents ytd-item-section-renderer>div#contents a#video-title')
        link = [web_element.get_attribute('href')]
        links += link
        count += 1
    driver.quit()
    return links

# writes text file with search URLs to specified directory 
def write_url(links):
    with open(PATH_LINKS, 'w') as link_file:
        content = '\n'.join(links)
        link_file.write(content)

# runs batch file to launch yt-dl with correct parameters
def download():
    os.system(PATH_BAT)

def main():
    create_dir()
    api = api_connect()
    songs = get_tracks(api)
    tracks, artists = parse_tracks(songs)
    write_df(tracks, artists)
    search_params = concat_search()
    driver = webdriver_init()
    links = query_links(driver, search_params)
    write_url(links)
    download()

main()
