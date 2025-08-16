import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from spotipy import Spotify
import lxml
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
client_key = os.getenv("client_key")
client_secret = os.getenv("client_secret")
uri = "http://127.0.0.1:8888/callback"

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=client_key,
    client_secret=client_secret,
    redirect_uri=uri,
    scope="playlist-modify-private",
    cache_path="token.txt"
))


ask = input("Which year do you wanna travel to? Type the date in this format YYY-MM-DD: ")
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

response = requests.get(f"https://www.billboard.com/charts/hot-100/{ask}/",headers=headers)
text = response.text
soup = BeautifulSoup(text, "lxml")
content = soup.find_all(name="h3",class_="c-title a-font-basic u-letter-spacing-0010 u-max-width-397 lrv-u-font-size-16 lrv-u-font-size-14@mobile-max u-line-height-22px u-word-spacing-0063 u-line-height-normal@mobile-max a-truncate-ellipsis-2line lrv-u-margin-b-025 lrv-u-margin-b-00@mobile-max")
all_names = [i.text.strip() for i in content]
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user= user_id, name=f"{ask} Billboard 100",public=False)
for i in all_names:
    try:
        result = sp.search(q= i,type= "track",limit=1)
        track_uri = result["tracks"]["items"][0]["uri"]
        sp.playlist_add_items(playlist_id=playlist["id"], items=[track_uri])

    except Exception as e:
        print(f"There was en error: {e} in adding the track")

print("Tracks added")