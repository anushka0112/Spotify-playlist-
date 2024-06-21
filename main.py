from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date=input("Which year do you want to travel to?Type the date in this format YYYY-MM-DD:")

url="https://www.billboard.com/charts/hot-100/"

response=requests.get(url+date)
website_html=response.text

soup=BeautifulSoup(website_html,"html.parser")
songs=soup.select("li ul li h3")
songs_titles = [song.getText().strip() for song in songs]
print(songs_titles)

client_id="Add your client id"
client_secret="**SECRET KEY**"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    ))
user_id = sp.current_user()["id"]
song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = date.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        print(uri)
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
