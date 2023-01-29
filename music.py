import spotipy
from spotipy.oauth2 import SpotifyOAuth

import streamlit as st
import webbrowser


st.set_page_config(page_title="MusiCurator - Curated Playlists for Music Lovers", page_icon="musical_note")


# Spotify credentials
c_id = "a3a7f70023c24444a54c0946ba55ddbb"
c_sec = "da5a2e5423e14b7293ecc917fdc43ce9"

<<<<<<< HEAD
sp_oauth = SpotifyOAuth(client_id=c_id,
                        client_secret=c_sec,
                        redirect_uri = "http://localhost:8000/callback",                              
                        scope=['user-library-read', 'app-remote-control', 'playlist-modify-public'])

# redirected_url = 'https://example.com/redirect'
# webbrowser.open(redirected_url)

token = sp_oauth.get_access_token()

sp = spotipy.Spotify(auth_manager=sp_oauth)

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
#                                                client_secret=c_sec,
#                                                redirect_uri = "http://localhost:8000/callback",                              
#                                                scope=['user-library-read', 'app-remote-control', 'playlist-modify-public']))
=======
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
#                                                client_secret=c_sec,
#                                                redirect_uri = "http://localhost:8080",                              
#                                                scope=['user-library-read','user-read-private', 'app-remote-control', 'playlist-modify-public']))
# >>>>>>> 03d315981827a119b011a96ef5b95e8c57c3eb08


st.markdown("<h1 align='center'>MusiCurator", unsafe_allow_html=True)

st.write('<div align="center">"MusiCurator" - Your personal music concierge. Just input your favorite artist, song, and genre, and let our app curate the perfect playlist for you. Discover new music, save and listen offline, all in one convenient app. Give your ears a treat with MusiCurator.',  unsafe_allow_html=True)


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
    # artist = input("Enter an artist of your choice: ")
    # song = input("Enter a song that you love: ")
    # genre = input("Enter the genre for the playlist: ")


    # Search for an artist
    artist_results = sp.search(q='artist:' + artist, type='artist')
    artist = artist_results['artists']['items'][0]
    artist_id = artist['id']

    # Search for a song
    # song_results = sp.search(q='track:' + song,type='track')
    # song = song_results['tracks']['items'][0]
    # song_id = song['id']
    
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


# get_recommendation()
