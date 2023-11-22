from youtubesearchpython import VideosSearch
from youtube.mapper import YoutubeMapper
import yt_dlp


class YoutubeModel:
    def search_video(self, name: str) -> str:
        data = VideosSearch(f"{name} audio", limit=1)
        link = YoutubeMapper().map_video_by_link(data.result())
        print(f"[MP3SpotifyPlaylist] Found YT Link for {name}")
        return link

    def download_audio(self, youtube_url: str) -> None:
        output = "/songs"

        video_info = yt_dlp.YoutubeDL().extract_info(url=youtube_url, download=False)

        try:
            for singleVideoInfo in video_info["entries"]:
                self._make_download(singleVideoInfo, output)
        except KeyError:
            self._make_download(video_info, output)

    def _make_download(self, videoInfo, path):
        try:
            filename = f"{path}/{videoInfo['title']}.mp3"
            options = {
                "format": "bestaudio/best",
                "keepvideo": False,
                "outtmpl": filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([videoInfo["webpage_url"]])
        except:
            print("error occured with one video")
