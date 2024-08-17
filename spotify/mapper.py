import re
from config import config


class SpotifyMapper:
    def map_track_names_from_playlist(self, tracks) -> [str]:
        song_names = []

        for song in tracks:
            song_name = song["track"]["name"]
            artist = song["track"]["artists"][0]["name"]

            song = self._sanitize_song_name(f"{artist} - {song_name}")

            if artist in config.skip_artists:
                print(f'[SpotifyPlaylistToMP3] Skipping "{song}"')
                continue

            song_names.append(song)

        return song_names

    def _sanitize_song_name(self, song):
        invalid_chars = r'[\/:*?"<>|]'
        sanitized_filename = re.sub(invalid_chars, "_", song)
        return sanitized_filename
