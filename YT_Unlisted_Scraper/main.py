import math
import msvcrt
import func
import time
import requests

# public link: https://www.youtube.com/watch?v=Ipw0NZThxKo
# unlisted link: https://www.youtube.com/watch?v=RFWk_NDRSWU

'''
Sources used:
https://wiki.archiveteam.org/index.php/YouTube/Technical_details#:~:text=8%20References-,ID%20formats,Za%2Dz0%2D9%2D_%20.

'''

URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]
cur_URL = ""

init_ID = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")

unlisted_videos = open("YT_Unlisted_Scraper/unlistedVideos.txt","a")

while(True):
    if(init_ID == "NONE"): # No cur_ID change
        break
    elif(URL_base in init_ID and len(init_ID) == 43): # Valid YT link input
        init_ID = init_ID[32:]

        # Testing ID for validity
        valid_ID = func.test_validity(init_ID)

        if(valid_ID == False): # Invalid input
            print(f"{init_ID} is not a valid input. Please try again.")
            init_ID = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")
        else: # Valid input
            cur_ID = func.initialize_bit_ID(init_ID)
            break
    elif(len(init_ID) == 11): # Valid ID input
        # Testing ID for validity
        valid_ID = func.test_validity(init_ID)

        if(valid_ID == False): # Invalid input
            print(f"{init_ID} is not a valid input. Please try again.")
            init_ID = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")
        else: # Valid input
            cur_ID = func.initialize_bit_ID(init_ID)
            break
    else: # Invalid input
        print(f"{init_ID} is not a valid input. Please try again.")
        init_ID = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")

cur_URL = func.create_url(cur_ID)

print("")
print(f"Current URL: {cur_URL}")
print(f"Current ID: {cur_ID}")
print("")

print("Scraping is starting. Press 'q' to stop program.")
print("")

# Scraping begins
while(True):
    time_start = time.time()

    # Stop Conditions
    if(cur_ID[0] == "FINISHED"): # Check for no more IDs
        print("Ran out of IDs (all values maxed out), stopping program.")
        break

    if(msvcrt.kbhit()): # Check for keyboard inputs
        if(msvcrt.getwch() == "q"):
            print("Keyboard input detected, stopping program.")
            break

    is_unlisted = func.check_for_unlisted(cur_URL)

    if(is_unlisted):
        unlisted_videos.write(cur_URL + "\n")
        
        print(f"Unlisted Video Found!")
    
    print(f"Current URL: {cur_URL}")
    print(f"Current ID: {cur_ID}")
    print(f"Loop Time: {time.time() - time_start}")
    print(f"Press 'q' to stop the program.")
    print("")

    cur_ID = func.increment_ID(cur_ID)
    cur_URL = func.create_url(cur_ID)

# Write code for printing out unlisted videos based on text file