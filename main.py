from dotenv import load_dotenv

load_dotenv()
from spotify import SpotifyMapper, SpotifyRequest
from youtube import YoutubeModel


def start():
    try:
        print("[SpotifyPlaylistToMP3] Starting application!")

        playlist_data = SpotifyRequest().get_playlist_tracks()
        if not playlist_data:
            raise ValueError("Playlist not found!")

        songs_list = SpotifyMapper().map_track_names_by_artist(playlist_data)
        if not songs_list:
            raise ValueError("Playlist is empty!")

        youtube = YoutubeModel()

        failed_songs = []
        for artist, songs in songs_list.items():
            for song in songs:
                artist_song_name = f"{artist} - {song}"

                url = youtube.search_video(artist_song_name)
                if not url:
                    failed_songs.append(artist_song_name)
                    continue

                success = youtube.download_audio(url, artist_song_name, artist)
                if not success:
                    failed_songs.append(artist_song_name)
                    continue

        with open("failed.txt", "w") as f:
            for song in failed_songs:
                f.write(f"{song} \n")

        print("[SpotifyPlaylistToMP3] Application finished successfully!")
    except Exception as error:
        print(f"[SpotifyPlaylistToMP3] Application failed: {error}")


if __name__ == "__main__":
    start()
