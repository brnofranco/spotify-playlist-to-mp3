from dotenv import load_dotenv

load_dotenv()
from spotify import SpotifyMapper, SpotifyRequest
from youtube import YoutubeModel


def start():
    try:
        print("[SpotifyPlaylistToMP3] Starting application!")

        playlist_data = SpotifyRequest().get_playlist_tracks()
        songs_list = SpotifyMapper().map_track_names_from_playlist(playlist_data)
        youtube = YoutubeModel()

        count = 1
        for song in songs_list:
            url = youtube.search_video(song)
            youtube.download_audio(url, song, count)
            count += 1

        print("[SpotifyPlaylistToMP3] Starting finished successfully!")
    except Exception as error:
        print(f"[SpotifyPlaylistToMP3] Application failed: {error}")


if __name__ == "__main__":
    start()
