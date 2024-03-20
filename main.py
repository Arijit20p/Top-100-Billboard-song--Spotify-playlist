import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client import CLIENT_ID,CLIENT_SECRET
from scrap import scrapping

CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
END = f"https://api.spotify.com/v1/users/{CLIENT_ID}/playlists"



# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_names = scrapping(date)


#Spotify Authentication
auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()["id"]

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
