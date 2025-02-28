import requests
import re
import time
import random
import multiprocessing

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def check_unlisted_youtube(video_url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(video_url, headers=headers)

        # # Save the page HTML for debugging
        # with open(f"YT_unlisted_scraper/{video_url.split('=')[-1]}.html", "w", encoding="utf-8") as file:
        #     file.write(response.text)

        if response.status_code != 200:
            return video_url, "Video not found or private"
        
        gone = re.search(r"This video isn't available anymore", response.text)
        country = re.search(r'"availableCountries":', response.text)

        # Retry until we get a valid response
        while not country:
            if gone:
                return video_url, "This video is no longer available (deleted or private)."
            response = requests.get(video_url, headers=headers)
            gone = re.search(r"This video isn't available anymore", response.text)
            country = re.search(r'"availableCountries":', response.text)

        # Search for 'isUnlisted' property
        match = re.search(r'"isUnlisted":(true|false)', response.text)
        if match:
            return video_url, "Unlisted" if match.group(1) == "true" else "Public"
        
        return video_url, "Could not determine (possibly private or deleted)"
    
    except Exception as e:
        return video_url, f"Error: {e}"

def process_videos(video_urls, num_processes=4):
    """Runs the YouTube checks in parallel using multiprocessing."""
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(check_unlisted_youtube, video_urls)

    return results

# Example Usage
if __name__ == "__main__":
    start_time = time.time()

    # List of YouTube video URLs to check
    video_urls = [
        "https://www.youtube.com/watch?v=AAAAAAAAAAA",
        "https://www.youtube.com/watch?v=BBBBBBBBBBB",
        "https://www.youtube.com/watch?v=CCCCCCCCCCC",
        "https://www.youtube.com/watch?v=DDDDDDDDDDD"
    ]

    # Run multiprocessing check
    results = process_videos(video_urls, num_processes=4)

    # Print results
    for video_url, status in results:
        print(f"{video_url} ➝ {status}")

    print(f"Total time taken: {time.time() - start_time:.2f} seconds")