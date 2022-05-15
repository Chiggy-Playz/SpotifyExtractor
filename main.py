from itsdangerous import json
import tekore as tk
import toml

with open("config.toml") as f:
    config = toml.load(f)

client_id, client_secret = (
    config["Secrets"]["client_id"],
    config["Secrets"]["client_secret"],
)
redirect_uri = "http://localhost:8877"

token = tk.prompt_for_user_token(
    client_id, client_secret, redirect_uri, scope=tk.scope.read
)
data = {}

spotify = tk.Spotify(token)
user_id = spotify.current_user().id

tracks = spotify.saved_tracks(limit=50)
saved_tracks = [
    {"id": t.track.id, "name": t.track.name} for t in spotify.all_items(tracks)
]
data["SavedTracks"] = saved_tracks

playlists = list(spotify.all_items(spotify.playlists(user_id, limit=50)))
for playlist in playlists:
    playlist_tracks = spotify.all_items(spotify.playlist_items(playlist.id))
    data[playlist.name] = [
        {
            "name": t.track.name,
            "id": t.track.id,
        }
            for t in playlist_tracks if not t.is_local
    ]

with open("output.json", "w") as f:
    json.dump(data, f, indent=4)
