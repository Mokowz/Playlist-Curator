import requests
import webbrowser
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import streamlit as st

from urllib.parse import urlparse

c_id = "a3a7f70023c24444a54c0946ba55ddbb"
c_sec = "da5a2e5423e14b7293ecc917fdc43ce9"
r_uri = "http://localhost:8000"

# Get authorization
auth_endpoint = "https://accounts.spotify.com/authorize"

auth_params = {
    "client_id": c_id,
    "response_type": "code",
    "redirect_uri": r_uri,
    "scope": "user-library-read playlist-modify-public playlist-modify-private user-library-modify"
}


auth_url = f"{auth_endpoint}?{requests.compat.urlencode(auth_params)}"

# Open the authorization URL in the user's default browser
webbrowser.open(auth_url)


# The url
call_url = st.text_input("Paste the url here: ")
parsed_url = urlparse(call_url)

query = parsed_url.query
auth_code = query.split("=")[1]

# print('Query:', parsed_url.query)
# auth_code

token_endpoint = "https://accounts.spotify.com/api/token"

data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": r_uri,
    "client_id": c_id,
    "client_secret": c_sec
}

response = requests.post(token_endpoint, data=data)
# response

sp_oauth = SpotifyOAuth(client_id=c_id,
                        client_secret=c_sec,
                        redirect_uri = r_uri,                              
                        scope=['user-library-read', 'app-remote-control', 'playlist-modify-public'])

# token = "BQAOf6tsmVTh15ivS01e1rRRraKrqxYP2m2k0VVvQUZTWzC55NmlxJ4DHd2UuNXXbPLn0qY4oV5zGgdpyhXEM1-XyMR8xSI9EX1CwBZcpH6DpQFITDkbyzFKdIlvA9HrA5WtcY1UGjw_sdkbyLMQ0g_aUS6au2VbMwZSswiUXAWd9LeGXk4h9xZTl1CXPTVPgdBA"
sp = spotipy.Spotify(auth_manager=sp_oauth)

st.write('<div align="center">Copy the code of the website where you will be redirected and paste it here.',  unsafe_allow_html=True)


# Get user input
playlist_name = st.text_input("Enter the playlist's name: ")
artist = st.text_input("Enter an artist of your choice: ")
genre = st.text_input("Enter the genre of the playlist: ")

# Get the user id of the current user
def get_user_id():
    user_id = sp.current_user()["id"]

    if not user_id:
        user_id = input("Enter your spotify user id: ")

    return user_id
    

# Create the playlist
def playlist_info(playlist_name):
    # playlist_name = input("Enter the playlist's name: ")
    playlist_description = 'A playlist generated from recommendations'

    playlist = sp.user_playlist_create(user=get_user_id(),
                                    name=playlist_name,
                                    description=playlist_description)
    playlist_id = playlist["id"]

    return playlist_id

# Get recommendations based on artist's name, song or genre
def get_recommendation(artist, genre, playlist_name):

    # Search for an artist
    artist_results = sp.search(q='artist:' + artist, type='artist')
    artist = artist_results['artists']['items'][0]
    artist_id = artist['id']
    
    # Genre
    genre = genre.lower()
    
    # seed_tracks=[song_id],
    results = sp.recommendations(seed_artists=[artist_id],  seed_genres=[genre])
    
    tracks_uri = [track["uri"] for track in results["tracks"]]
    
    # Add the recommended songs to the playlist
    sp.playlist_add_items(playlist_id=playlist_info(playlist_name), items=tracks_uri)


# After submitting now run the function
if st.button("Curate Playlist"):
    get_recommendation(artist, genre, playlist_name)