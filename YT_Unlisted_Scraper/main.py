import msvcrt
import func
import time

# public link: https://www.youtube.com/watch?v=Ipw0NZThxKo
# unlisted link: https://www.youtube.com/watch?v=RFWk_NDRSWU

# Variable Creation
URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]

cur_URL = ""

average_loop_time = [0,0,0,0,0,0,0,0,0,0]

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

    while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
        print("")
        print(f"'{ready_to_continue}' is not a valid input. Please try again.")
        init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

    if(ready_to_continue == "STOP"):
        quit()
    else:
        with open("YT_unlisted_scraper/LastURL.txt","r") as init_file:
                init_URL = init_file.readline().strip("\n")

        while(True):
            if(URL_base in init_URL and len(init_URL) == 43):
                init_ID = init_URL[32:]

                valid_ID = func.test_validity(init_ID)

                if(valid_ID == False): # Invalid input
                    print("")
                    print(f"'{init_URL}' is not a valid input. Please try again.")
                    print("Please put the URL in the first line of 'YT_unlisted_scraper/LastURL.txt'")
                    ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")

                    while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                        print("")
                        print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                        init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                    if(ready_to_continue == "STOP"):
                        quit()
                    else:
                        with open("YT_unlisted_scraper/LastURL.txt","r") as init_file:
                            init_URL = init_file.readline().strip("\n")
                else: # Valid input
                    cur_ID = func.initialize_bit_ID(init_ID)
                    break
            else:
                print("")
                print(f"'{init_URL}' is not a valid input. Please try again.")
                print("Please put the URL in the first line of 'YT_unlisted_scraper/LastURL.txt'")
                ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")

                while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                    print("")
                    print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                    init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                if(ready_to_continue == "STOP"):
                    quit() 
                else:
                    with open("YT_unlisted_scraper/LastURL.txt","r") as init_file:
                        init_URL = init_file.readline().strip("\n")
else:
    init_ID = input("Input ID to start at or 'NONE'. (Input YouTube link, YouTube ID, or 'NONE')")

    while(True):
        if(init_ID == "NONE"): # No cur_ID change
            break
        elif(URL_base in init_ID and len(init_ID) == 43): # Valid YT link input
            init_ID = init_ID[32:]

            # Testing ID for validity
            valid_ID = func.test_validity(init_ID)

            if(valid_ID == False): # Invalid input
                print("")
                print(f"'{init_ID}' is not a valid input. Please try again.")
                init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")
            else: # Valid input
                cur_ID = func.initialize_bit_ID(init_ID)
                break
        elif(len(init_ID) == 11): # Valid ID input
            # Testing ID for validity
            valid_ID = func.test_validity(init_ID)

            if(valid_ID == False): # Invalid input
                print("")
                print(f"'{init_ID}' is not a valid input. Please try again.")
                init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")
            else: # Valid input
                cur_ID = func.initialize_bit_ID(init_ID)
                break
        else: # Invalid input
            print("")
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
public_videos_count = 0
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
            print("Toggling outputs.")
            data_output_minimal = not data_output_minimal

    if(URLs_tested != 0):
        cur_ID = func.increment_ID(cur_ID)
        cur_URL = func.create_url(cur_ID)

    video_type = func.check_for_unlisted(cur_URL)

    if(video_type == "Unlisted"):
        with open("YT_Unlisted_Scraper/UnlistedVideos.txt","a") as unlisted_videos:
            unlisted_videos.write(cur_URL + "\n")
        
        unlisted_videos_count += 1
        
        print(f"Unlisted Video Found!")
        print(f"Current URL: {cur_URL}")
        print(f"Current ID: {cur_ID}")
    elif(video_type == "Public"):
        with open("YT_Unlisted_Scraper/PublicVideos.txt","a") as unlisted_videos:
            unlisted_videos.write(cur_URL + "\n")
        
        public_videos_count += 1
        
        print(f"Public Video Found!")
        print(f"Current URL: {cur_URL}")
        print(f"Current ID: {cur_ID}")

    if(data_output_minimal):
        if(URLs_tested % 10 == 0):
            print(f"URLs tested: {URLs_tested}")
            print(f"Average loop time: {func.average_list(average_loop_time):.4f} seconds.")
            print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
            print("")
    else:
        print(f"URLs tested: {URLs_tested}")
        print(f"Current URL: {cur_URL}")
        print(f"Current ID: {cur_ID}")
        print(f"Average loop time: {func.average_list(average_loop_time):.4f} seconds.")
        print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
        print("")

    with open("YT_unlisted_scraper/LastURL.txt", "w") as file:
        file.write(cur_URL)

    del average_loop_time[0]
    average_loop_time.append(time.time() - time_start)

    URLs_tested += 1

with open("YT_unlisted_scraper/TotalURLsTested.txt","r") as total_tested_file:
    total_tested = int(total_tested_file.readline().strip("\n"))
    total_tested += URLs_tested

with open("YT_unlisted_scraper/TotalURLsTested.txt","w") as total_tested_file:
    total_tested_file.write(str(total_tested))

print("")
print(f"Total Time Elapsed: {time.time() - loop_start_time:.4f} seconds.")
print(f"Total URLs Tested This Execution: {URLs_tested}")
print(f"Total URLs Tested: {total_tested}")
print(f"Total Unlisted Videos Found: {unlisted_videos_count}")
print(f"Total Public Videos Found: {public_videos_count}")
print(f"Last URL tested: {cur_URL}")
print(f"Last ID tested: {cur_ID}")