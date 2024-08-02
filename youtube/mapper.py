from youtubesearchpython import VideosSearch


class YoutubeMapper:
    def get_video_link(self, data: VideosSearch) -> str:
        return data["result"][0]["link"]

    def get_video_title(self, data: VideosSearch) -> str:
        return data["result"][0]["title"]
