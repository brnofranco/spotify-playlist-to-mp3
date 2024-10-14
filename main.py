from dotenv import load_dotenv

load_dotenv()
from spotify import SpotifyMapper, SpotifyRequest
from youtube import YoutubeModel
from config import config


def start():
    try:
        print("[SpotifyPlaylistToMP3] Starting application!")

        playlist_data = SpotifyRequest().get_playlist_tracks()
        if not playlist_data:
            raise ValueError("Playlist not found!")

        songs_list = SpotifyMapper().map_track_names_from_playlist(playlist_data)
        if not songs_list:
            raise ValueError("Playlist is empty!")

        youtube = YoutubeModel()

        if config.reverse:
            songs_list.reverse()

        song_number = 1
        for song in songs_list:
            url = youtube.search_video(song)
            if not url:
                continue

            success = youtube.download_audio(url, song, song_number)
            if not success:
                continue

            song_number += 1

        print("[SpotifyPlaylistToMP3] Application finished successfully!")
    except Exception as error:
        print(f"[SpotifyPlaylistToMP3] Application failed: {error}")


if __name__ == "__main__":
    start()
