import base64
from typing import Any
import requests

from config import config


class SpotifyRequest:
    def __init__(self) -> None:
        self.bearer_token = self._get_token()

    def _get_token(self) -> str:
        print("[MP3SpotifyPlaylist] Getting Spotify token")
        client_id = config.spotify_client_id
        client_secret = config.spotify_client_secret

        credentials = f"{client_id}:{client_secret}"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        auth_url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": "Basic " + base64_credentials}
        payload = {"grant_type": "client_credentials"}

        response = requests.post(auth_url, headers=headers, data=payload)
        if response.status_code == 200:
            token = f"Bearer {response.json().get('access_token')}"
            print("[MP3SpotifyPlaylist] Spotify token successfully got")
            return token
        else:
            print(f"[MP3SpotifyPlaylist] Spotify token error {response.status_code}")
            print(response.text)

    def _request(self, path: str, params: Any) -> Any:
        url = f"https://api.spotify.com{path}"

        response = requests.get(
            url,
            headers={"Authorization": self.bearer_token},
            params=params,
        )

        if response.ok:
            print(response.status_code)
            return response.json()
        else:
            print(response.text)
            return response.text

    def get_playlist_tracks(self) -> [object]:
        print("[MP3SpotifyPlaylist] Getting song names from playlist")
        tracks = []

        playlist_url = config.spotify_playlist_url
        playlist_id = playlist_url.split("playlist/")[1]
        path = f"/v1/playlists/{playlist_id}/tracks"

        limit = 100
        offset = 0

        while len(tracks) == offset:
            params = {"offset": offset, "limit": limit}
            response = self._request(path=path, params=params)

            if response is not str:
                items = response.get("items")

                if len(items) == 0:
                    break

                for item in items:
                    tracks.append(item)
                if len(items) == limit:
                    offset += 100
            else:
                print(f"[MP3SpotifyPlaylist] Get song names error: {response.status_code}")
                print(response.text)

        print("[MP3SpotifyPlaylist] Got all names")
        return tracks
