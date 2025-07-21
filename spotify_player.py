#spotify_player.py
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Debugging
print(f"🐍 Using Python: {sys.executable}")
print(f"📦 Installed Packages: {sys.path}")

# Spotify API Credentials
SPOTIPY_CLIENT_ID = "c32801c4a2754f6db933be5b6d89e7d3"
SPOTIPY_CLIENT_SECRET = "7b00e4e72182431d9b783f375add6471"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

# Initialize Spotify Client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-modify-playback-state,user-read-playback-state"))

# Mood to Playlist Mapping
mood_playlist = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
    "sad": "spotify:playlist:37i9dQZF1DX7qK8ma5wgG1",
    "neutral": "spotify:playlist:37i9dQZF1DWXJfnUiYjUKT",
    "angry": "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP",
}

# Get mood from command-line argument
if len(sys.argv) < 2:
    print("❌ Error: No mood provided!")
    sys.exit(1)

mood = sys.argv[1]
print(f"🎵 Playing music for mood: {mood}")

playlist_uri = mood_playlist.get(mood, mood_playlist["neutral"])

# Get active device
devices = sp.devices()
device_list = devices.get("devices", [])

if not device_list:
    print("❌ No active device found! Open Spotify and play a song first.")
    sys.exit(1)

# Select the first available device
device_id = device_list[0]["id"]
print(f"✅ Using Device: {device_list[0]['name']} ({device_id})")

# Play music on Spotify
try:
    sp.start_playback(device_id=device_id, context_uri=playlist_uri)
    print(f"✅ Now playing: {mood} music!")
except Exception as e:
    print(f"❌ Error: {e}")
