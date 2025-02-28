import requests
import re
import time
import random

def check_unlisted_youtube(video_url):
    USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"]


    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    try:
        # Fetch the YouTube page source
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(video_url, headers=headers)
        

        with open("YT_unlisted_scraper/youtube_page.html","w",encoding = "utf-8") as file:
            file.write(response.text)

        if response.status_code != 200:

            return "Video not found or private"
        
        gone = re.search(r"This video isn't available anymore", response.text)
        country = re.search(r'"availableCountries":', response.text)

        while(not country):
            if(gone):
                print(gone.group(0))
                return("This video is no longer available (deleted or private).")
            response = requests.get(video_url, headers=headers)
            gone = re.search(r"This video isn't available anymore", response.text)
            country = re.search(r'"availableCountries":', response.text)
            print("bad, try again")
            with open("YT_unlisted_scraper/youtube_page.html","w",encoding = "utf-8") as file:
                file.write(response.text)
            time.sleep(1)

        with open("YT_unlisted_scraper/youtube_page.html","w",encoding = "utf-8") as file:
            file.write(response.text)

        # Search for the 'isUnlisted' property in the HTML source
        match = re.search(r'"isUnlisted":(true|false)', response.text)

        if match:

            return "Unlisted" if match.group(1) == "true" else "Public"
        

        return "Could not determine (possibly private or deleted)"
    
    except Exception as e:
        return f"Error: {e}"

# Example Usage
start_time = time.time()

f = open("file.html","w")

video_url = "https://www.youtube.com/watch?v=AAAAAAAAAAA"  # Replace with actual video URL
video_status = check_unlisted_youtube(video_url)
print(f"Video status: {video_status}")
print(time.time()-start_time)

# https://www.youtube.com/watch?v=AAAAAAAAAAA