from collections import defaultdict
import re
from config import config


class SpotifyMapper:
    def map_track_names_by_artist(self, tracks) -> dict[str, set]:
        songs_dict = defaultdict(set)

        for song in tracks:
            artist = self._sanitize_name(song["track"]["artists"][0]["name"])
            song_name = self._sanitize_name(song["track"]["name"])

            if artist in config.skip_artists:
                print(f'[SpotifyPlaylistToMP3] Skipping "{artist} - {song_name}"')
                continue

            songs_dict[artist].add(song_name)

        return songs_dict

    def map_track_names_in_order(self, tracks) -> [str]:
        songs = []

        counter = 1
        for song in tracks:
            artist = self._sanitize_name(song["track"]["artists"][0]["name"])
            song_name = self._sanitize_name(song["track"]["name"])

            songs.append(f"{counter:03d} {artist} - {song_name}")
            counter += 1

        return songs

    def _sanitize_name(self, name: str):
        invalid_chars = r'[\/:*?"<>|]'
        sanitized_filename = re.sub(invalid_chars, "_", name)
        return sanitized_filename
