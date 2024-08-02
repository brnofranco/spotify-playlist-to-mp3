import os
from youtubesearchpython import VideosSearch
from config import config
from youtube.mapper import YoutubeMapper
from pytube import YouTube
from moviepy.editor import VideoFileClip


class YoutubeModel:
    def search_video(self, name: str) -> str:
        search_name = f"{name} - official audio"
        data = VideosSearch(search_name, limit=1)
        print(f'[SpotifyPlaylistToMP3] Searching for "{search_name}"')

        link = YoutubeMapper().get_video_link(data.result())
        video_title = YoutubeMapper().get_video_title(data.result())
        print(f'[SpotifyPlaylistToMP3] Found YT Link for "{name}" - YT: "{video_title}"')

        return link

    def download_audio(self, youtube_url: str, song_name: str, index: int) -> None:
        try:
            output = config.download_path_songs
            audio_path = output + "/" + f"{index:03}" + " " + song_name + ".mp3"

            if os.path.isfile(audio_path):
                print(f'[SpotifyPlaylistToMP3] "{song_name}" already downloaded')
                return

            # Thats the only way file song worked in my car radio
            youtube = YouTube(youtube_url)
            video_stream = youtube.streams.get_highest_resolution()
            video_path = video_stream.download(output)
            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path, codec="mp3")
            video_clip.close()

            os.remove(video_path)
        except Exception as error:
            print(f'[SpotifyPlaylistToMP3] "{song_name}" failed to download: {error}')
            print(f'[SpotifyPlaylistToMP3] Skipping "{song_name}"')
