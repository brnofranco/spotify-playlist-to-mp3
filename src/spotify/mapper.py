class SpotifyMapper:
    def map_track_names_from_playlist(self, tracks) -> [str]:
        song_names = []
        for song in tracks:
            song_names.append(song["track"]["name"])
        return song_names
