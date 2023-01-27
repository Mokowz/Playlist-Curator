import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


# Spotify credentials
c_id = "a3a7f70023c24444a54c0946ba55ddbb"
c_sec = "da5a2e5423e14b7293ecc917fdc43ce9"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
                                               client_secret=c_sec,
                                               redirect_uri = "http://localhost:8080",                              
                                               scope=['user-library-read', 'app-remote-control', 'playlist-modify-public']))


# Get the user id of the current user
def get_user_id():
    user_id = sp.current_user()["id"]

    if not user_id:
        user_id = input("Enter your spotify user id: ")

    return user_id
    


# Create the playlist
def playlist_info():
    playlist_name = input("Enter the playlist's name: ")
    playlist_description = 'A playlist generated from recommendations'

    playlist = sp.user_playlist_create(user=get_user_id(),
                                    name=playlist_name,
                                    description=playlist_description)
    playlist_id = playlist["id"]

    return playlist_id




# Get recommendations based on artist's name, song or genre
def get_recommendation():
    artist = input("Enter an artist of your choice: ")
    # song = input("Enter a song that you love: ")
    genre = input("Enter the genre for the playlist: ")


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
    sp.playlist_add_items(playlist_id=playlist_info(), items=tracks_uri)



get_recommendation()