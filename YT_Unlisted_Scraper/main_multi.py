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

# Variable Creation
URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]
cur_URL = ""

average_loop_time = [0,0,0,0,0,0,0,0,0,0]

unlisted_videos = open("YT_Unlisted_Scraper/UnlistedVideos.txt","a")

data_output_minimal = True

# Initializing the URL
init_from_file = input("Would you like to start the scraper using an URL in a file? ('Y' or 'N') ")
print("")

while(not (init_from_file == "Y") and not (init_from_file == "N")):
    print(f"'{init_from_file}' is not a valid input. Please try again.")
    init_from_file = input("Would you like to start the scraper using an URL in a file? ('Y' or 'N') ")

if(init_from_file == "Y"):
    print("Please put the URL in the first line of 'YT_unlisted_scraper/LastURL.txt'")
    ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
    print("")

    while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
        print(f"'{ready_to_continue}' is not a valid input. Please try again.")
        init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

    if(ready_to_continue == "STOP"):
        quit()
    else:
        init_file = open("YT_unlisted_scraper/LastURL.txt","r")
        init_URL = init_file.readline()
        init_URL = init_URL.strip()
        init_file.close()

        while(True):
            if(URL_base in init_URL and len(init_URL) == 43):
                init_ID = init_URL[32:]

                valid_ID = func.test_validity(init_ID)

                if(valid_ID == False): # Invalid input
                    print(f"'{init_URL}' is not a valid input. Please try again.")
                    print("Please put the URL in the first line of 'YT_unlisted_scraper/LastURL.txt'")
                    ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
                    print("")

                    while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                        print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                        init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                    if(ready_to_continue == "STOP"):
                        quit()
                    else:
                        init_file = open("YT_unlisted_scraper/LastURL.txt","r")
                        init_URL = init_file.readline.strip("\n")
                        init_file.close()
                else: # Valid input
                    cur_ID = func.initialize_bit_ID(init_ID)
                    break
            else:
                print(f"'{init_URL}' is not a valid input. Please try again.")
                print("Please put the URL in the first line of 'YT_unlisted_scraper/LastURL.txt'")
                ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
                print("")

                while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                    print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                    init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                if(ready_to_continue == "STOP"):
                    quit()
                else:
                    init_file = open("YT_unlisted_scraper/LastURL.txt","r")
                    init_URL = init_file.readline.strip("\n")
                    init_file.close()
else:
    init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")

    while(True):
        if(init_ID == "NONE"): # No cur_ID change
            break
        elif(URL_base in init_ID and len(init_ID) == 43): # Valid YT link input
            init_ID = init_ID[32:]

            # Testing ID for validity
            valid_ID = func.test_validity(init_ID)

            if(valid_ID == False): # Invalid input
                print(f"'{init_ID}' is not a valid input. Please try again.")
                init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")
            else: # Valid input
                cur_ID = func.initialize_bit_ID(init_ID)
                break
        elif(len(init_ID) == 11): # Valid ID input
            # Testing ID for validity
            valid_ID = func.test_validity(init_ID)

            if(valid_ID == False): # Invalid input
                print(f"'{init_ID}' is not a valid input. Please try again.")
                init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")
            else: # Valid input
                cur_ID = func.initialize_bit_ID(init_ID)
                break
        else: # Invalid input
            print(f"'{init_ID}' is not a valid input. Please try again.")
            init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")

cur_URL = func.create_url(cur_ID)

print("")
print(f"Current URL: {cur_URL}")
print(f"Current ID: {cur_ID}")
print("")

print("Scraping is starting. Press 'q' to stop program. Press 'o' to minimize outputs.")
print("")

URLs_tested = 0
unlisted_videos_count = 0
loop_start_time = time.time()

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
        if(msvcrt.getwch() == "o"):
            print("Toggling outputs")
            data_output_minimal = not data_output_minimal

    if(URLs_tested != 0):
        cur_ID = func.increment_ID(cur_ID)
        cur_URL = func.create_url(cur_ID)

    is_unlisted = func.check_for_unlisted(cur_URL)

    if(data_output_minimal):
        if(is_unlisted):
            unlisted_videos = open("YT_Unlisted_Scraper/UnlistedVideos.txt","a")
            unlisted_videos.write(cur_URL + "\n")
            unlisted_videos.close()
            unlisted_videos_count += 1
            
            print(f"Unlisted Video Found!")
            print(f"Current URL: {cur_URL}")
            print(f"Current ID: {cur_ID}")
        
        if(URLs_tested % 10 == 0):
            print(f"URLs tested: {URLs_tested}")
            print(f"Average loop time: {func.sum_list(average_loop_time):.4f} seconds")
            print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
            print("")
    else:
        if(is_unlisted):
            unlisted_videos = open("YT_Unlisted_Scraper/UnlistedVideos.txt","a")
            unlisted_videos.write(cur_URL + "\n")
            unlisted_videos.close()
            unlisted_videos_count += 1
            
            print(f"Unlisted Video Found!")
        
        print(f"Current URL: {cur_URL}")
        print(f"Current ID: {cur_ID}")
        print(f"Loop Time: {(time.time() - time_start):.4f} seconds")
        print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
        print("")

    with open("YT_unlisted_scraper/LastURL.txt", "w") as file:
        file.write(cur_URL)

    del average_loop_time[0]
    average_loop_time.append(time.time() - time_start)

    URLs_tested += 1

# Write code for printing out unlisted videos based on text file
print("")
print(f"Total Time Elapsed: {time.time() - loop_start_time}")
print(f"Total URLs Tested: {URLs_tested}")
print(f"Total Unlisted Videos: {unlisted_videos_count}")
print(f"Last URL tested: {cur_URL}")
print(f"Last ID tested: {cur_ID}")