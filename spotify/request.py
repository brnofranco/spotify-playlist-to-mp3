import base64
from typing import Any
import requests
from config import config


class SpotifyRequest:
    def __init__(self) -> None:
        self.bearer_token = self._get_token()

    def _get_token(self) -> str:
        print("[SpotifyPlaylistToMP3] Getting Spotify token")
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
            print("[SpotifyPlaylistToMP3] Get Spotify token successfully")
            return token
        else:
            print(f"[SpotifyPlaylistToMP3] Get Spotify token error {response.status_code}")
            print(response.text)

    def _request(self, path: str, params: Any) -> Any:
        url = f"https://api.spotify.com{path}"

        response = requests.get(
            url,
            headers={"Authorization": self.bearer_token},
            params=params,
        )

        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def get_playlist_tracks(self) -> [object]:
        print("[SpotifyPlaylistToMP3] Getting song names from playlist")
        tracks = []

        playlist_url = config.spotify_playlist_url
        playlist_id = playlist_url.split("playlist/")[1]
        path = f"/v1/playlists/{playlist_id}/tracks"

        limit = 100
        offset = 0

        while len(tracks) == offset:
            params = {"offset": offset, "limit": limit}

            try:
                response = self._request(path=path, params=params)
                items = response.get("items")

                if len(items) == 0:
                    break

                for item in items:
                    tracks.append(item)
                if len(items) == limit:
                    offset += 100
            except Exception as error:
                print(f"[SpotifyPlaylistToMP3] Error trying to get song names: {error}")
                raise Exception("Failed to get song names")

        print("[SpotifyPlaylistToMP3] Got all song names")
        return tracks
