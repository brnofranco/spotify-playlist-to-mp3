import os


class Config:
    def __init__(self, envs) -> None:
        self.spotify_client_id: str = envs.get("SPOTIFY_CLIENT_ID", "")
        self.spotify_client_secret: str = envs.get("SPOTIFY_CLIENT_SECRET", "")
        self.spotify_playlist_url: str = envs.get("SPOTIFY_PLAYLIST_URL", "")
        self.download_path_songs: str = (
            envs.get("CUSTOM_DOWNLOAD_PATH_SONGS", "") or f"{os.path.abspath( os.getcwd() )}/songs"
        )
        self.skip_artists: [str] = envs.get("SKIP_ARTISTS", "").split(",")


config = Config(os.environ)
