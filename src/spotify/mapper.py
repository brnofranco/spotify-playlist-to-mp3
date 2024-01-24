class SpotifyMapper:
    def map_track_names_from_playlist(self, tracks) -> [str]:
        song_names = []
        for song in tracks:
            song_name = song["track"]["name"]
            artist = song["track"]["artists"][0]["name"]
            song_names.append(artist + " - " + song_name)

        return song_names
