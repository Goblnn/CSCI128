import requests
import re
import time

def check_unlisted_youtube(video_url):
    try:
        # Fetch the YouTube page source
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(video_url, headers=headers)
        
        if response.status_code != 200:
            return "Video not found or private"

        # Search for the 'isUnlisted' property in the HTML source
        match = re.search(r'"isUnlisted":(true|false)', response.text)

        if match:
            return "Unlisted" if match.group(1) == "true" else "Public"
        
        return "Could not determine (possibly private or deleted)"
    
    except Exception as e:
        return f"Error: {e}"

# Example Usage
start_time = time.time()

video_url = "https://www.youtube.com/watch?v=RFWk_NDRSWU"  # Replace with actual video URL
video_status = check_unlisted_youtube(video_url)
print(f"Video status: {video_status}")
print(time.time()-start_time)