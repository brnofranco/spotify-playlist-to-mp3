from uu import Error
from youtubesearchpython import VideosSearch
from youtube.mapper import YoutubeMapper
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os


class YoutubeModel:
    def search_video(self, name: str) -> str:
        data = VideosSearch(f"{name} audio", limit=1)
        link = YoutubeMapper().map_video_by_link(data.result())
        print(f"[MP3SpotifyPlaylist] Found YT Link for {name}")
        return link

    def download_audio(self, youtube_url: str, song_name: str, index: int) -> None:
        current_path = os.path.abspath(os.getcwd())
        output = current_path + "/songs"

        try:
            yt = YouTube(youtube_url)
            video_stream = yt.streams.get_highest_resolution()
            video_path = video_stream.download(output)

            audio_path = output + "/" + str(index) + ". " + song_name + ".mp3"

            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path, codec="mp3")
            video_clip.close()

            os.remove(video_path)
        except:
            print("não foi possivel baixar")
