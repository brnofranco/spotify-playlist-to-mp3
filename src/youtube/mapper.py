from youtubesearchpython import VideosSearch


class YoutubeMapper:
    def map_video_by_link(self, data: VideosSearch) -> str:
        return data["result"][0]["link"]
