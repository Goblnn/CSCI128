import yt_dlp
import time

start_time = time.time()

def check_unlisted(youtube_url):
    ydl_opts = {
        "quiet": True,
        #"noplaylist": True,
        "skip_download": True,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            privacy_status = info.get("availability")  # Checks the availability status
            if privacy_status == "unlisted":
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            return None

# Example usage:
video_url = "https://www.youtube.com/watch?v=RFWk_NDRSWU"
is_unlisted = check_unlisted(video_url)

if is_unlisted is None:
    print("Failed to retrieve video information.")
elif is_unlisted:
    print("The video is unlisted.")
else:
    print("The video is public or private.")

print(time.time() - start_time)