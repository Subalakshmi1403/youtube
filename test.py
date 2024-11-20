from pytube import YouTube


from yt_dlp import YoutubeDL

def download_video_ytdlp(video_url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return "Download completed successfully"
    except Exception as e:
        return f"Error: {str(e)}"


# Test with your video URL
video_url = "https://www.youtube.com/watch?v=AAq06bS8UZM"
print(download_video_ytdlp(video_url))