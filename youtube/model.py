import os
from youtubesearchpython import VideosSearch
from config import config
from youtube.mapper import YoutubeMapper
from pytubefix import YouTube
from moviepy.editor import VideoFileClip


class YoutubeModel:
    def search_video(self, name: str) -> str:
        search_name = f"{name} - official audio"
        data = VideosSearch(search_name, limit=1).result()

        if not data["result"]:
            print(f'[SpotifyPlaylistToMP3] Warn: Not found YT Link for "{search_name}"')
            return

        print(f'[SpotifyPlaylistToMP3] Searching for "{search_name}"')
        link = YoutubeMapper().get_video_link(data)
        video_title = YoutubeMapper().get_video_title(data)
        print(f'[SpotifyPlaylistToMP3] Found YT Link for "{name}" - YT: "{video_title}"')

        return link

    def download_audio(self, youtube_url: str, artist_song_name: str, artist: str) -> bool:
        CLIENTS = {
            1: "ANDROID",
            2: "WEB",
            3: "WEB_EMBED",
            4: "WEB_MUSIC",
            5: "WEB_CREATOR",
            6: "WEB_SAFARI",
            7: "ANDROID_MUSIC",
            8: "ANDROID_CREATOR",
            9: "ANDROID_VR",
            10: "ANDROID_PRODUCER",
            11: "ANDROID_TESTSUITE",
            12: "IOS",
            13: "IOS_MUSIC",
            14: "IOS_CREATOR",
            15: "MWEB",
            16: "TV_EMBED",
            17: "MEDIA_CONNECT",
        }

        try:
            for _, client in CLIENTS.items():
                try:
                    output = f"{config.download_path_songs}/{artist}"

                    audio_file = f"/{artist_song_name}.mp3"

                    if os.path.isfile(output + audio_file):
                        print(f'[SpotifyPlaylistToMP3] "{artist_song_name}" already downloaded')
                        return True

                    # Thats the only way file song worked in my car radio
                    print(f'[SpotifyPlaylistToMP3] Trying to reach with "{client}" client')
                    youtube = YouTube(youtube_url, client)
                    video_stream = youtube.streams.get_highest_resolution()
                    video_path = video_stream.download(output)
                    video_clip = VideoFileClip(video_path)
                    video_clip.audio.write_audiofile(output + audio_file, codec="mp3")
                    video_clip.close()

                    os.remove(video_path)
                    return True
                except Exception as error:
                    print(
                        f'[SpotifyPlaylistToMP3] "{artist_song_name}" failed to download with "{client}": {error}'
                    )

        except Exception as error:
            print(f'[SpotifyPlaylistToMP3] Skipping "{artist_song_name}"')
            return False
