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

        failed_songs = []
        song_number = 1
        for song in songs_list:
            url = youtube.search_video(song)
            if not url:
                failed_songs.append(song)
                continue

            success = youtube.download_audio(url, song, song_number)
            if not success:
                failed_songs.append(song)
                continue

            song_number += 1

        with open("failed.txt", "w") as f:
            for song in failed_songs:
                f.write(f"{song} \n")

        print("[SpotifyPlaylistToMP3] Application finished successfully!")
    except Exception as error:
        print(f"[SpotifyPlaylistToMP3] Application failed: {error}")


if __name__ == "__main__":
    start()
