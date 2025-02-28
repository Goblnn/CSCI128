import requests
import re
import random

ID_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
last_ID_chars = "AEIMQUYcgkosw048"

URL_base = "https://www.youtube.com/watch?v="

USER_AGENTS =  [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def test_validity(init_ID):
    """
    Checks an inputted ID to make sure it follows the valid YouTube ID setup

    :param init_ID: ID in character form to validate
    :return: True if valid, False if invalid
    """

    valid_chars = True

    i = 0
    for i in range(len(init_ID) - 1):
        if(init_ID[i] not in ID_chars):
            valid_chars = False

    if(init_ID[10] not in last_ID_chars):
        valid_chars = False

    if(valid_chars == False): # Invalid input
        return False
    else: # Valid input
        return True

def initialize_bit_ID(ID):
    """
    Changes a YouTube ID inputted in character form into bit form

    :param ID: Character ID to initialize into 64 bit form
    :return: List of the characters in the ID in 64 bit form
    """

    new_ID = [0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    for i in range(len(ID) - 1):
        new_ID[i] = ID_chars.index(ID[i])
    
    new_ID[10] = last_ID_chars.index(ID[10])
    
    return new_ID

def initialize_char_ID(ID):
    """
    Changes a YouTube ID inputted in bit form into character form

    :param ID: 64 bit ID to initialize into character form
    :return: ID string using valid YouTube characters
    """
        
    new_ID = ""

    i = 0
    for i in range(len(ID) - 1):
        new_ID += ID_chars[ID[i]]
    
    new_ID += last_ID_chars[ID[10]]
    
    return new_ID

def create_url(ID):
    """
    Generates a YouTube video URL for use in scraping

    :param ID: 64 bit ID to use in URL creation
    :return: YouTube video URL
    """
    URL = ""
    URL += URL_base

    char_id = initialize_char_ID(ID)

    URL += char_id
    
    return URL

def check_for_unlisted(URL): # CHECK THIS FOR MAKING SURE IT GETS ALL PACKETS
    
        # Get YouTube page
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        site = requests.get(URL, headers=headers)
        
        with open("YT_unlisted_scraper/youtube_page.html","w",encoding = "utf-8") as file:
             file.write(site.text)

        # Check for proper page lookup
        if site.status_code != 200:
            return False

        country_tag = re.search(r'"availableCountries":', site.text)

        while(not country_tag):
            site = requests.get(URL, headers=headers)
            country_tag = re.search(r'"availableCountries":', site.text)
            print("bad, try again")

        # Search for 'isUnlisted' in the HTML
        vid_type = re.search(r'"isUnlisted":(true|false)', site.text)

        if vid_type:
            if(vid_type.group(1) == "true"):
                return True
            else:
                return False
        
        return False

def increment_ID(ID):
    ID_pos = 0

    while(True):
        ID[ID_pos] += 1

        if(ID[ID_pos] > 63 and ID_pos < 10):
            ID[ID_pos] = 0
            ID_pos += 1
        elif(ID[ID_pos] > 15 and ID_pos == 10):
            ID[0] = "FINISHED"
            break
        else:
            break
    
    return ID