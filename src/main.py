from dotenv import load_dotenv

load_dotenv()
from spotify import SpotifyMapper, SpotifyRequest
from youtube import YoutubeModel


def start():
    print("[MP3SpotifyPlaylist] Starting application!")

    playlist_data = SpotifyRequest().get_playlist_tracks()
    songs_list = SpotifyMapper().map_track_names_from_playlist(playlist_data)
    youtube = YoutubeModel()

    for song in songs_list:
        url = youtube.search_video(song)
        youtube.download_audio(url)


if __name__ == "__main__":
    start()
