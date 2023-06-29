import youtube_dl

def get_video_title(video_url):
    options = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_title = info.get('title', '')
    return video_title

# Example usage
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
title = get_video_title(video_url)
print("Video Title:", title)
