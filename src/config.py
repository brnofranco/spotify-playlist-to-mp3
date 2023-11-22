import os


class Config:
    def __init__(self, envs) -> None:
        self.spotify_client_id: str = envs.get("SPOTIFY_CLIENT_ID", "")
        self.spotify_client_secret: str = envs.get("SPOTIFY_CLIENT_SECRET", "")
        self.spotify_playlist_id: str = envs.get("SPOTIFY_PLAYLIST_ID", "")


config = Config(os.environ)
