import msvcrt
import multiprocessing
import func
import time

# public link: https://www.youtube.com/watch?v=Ipw0NZThxKo
# unlisted link: https://www.youtube.com/watch?v=RFWk_NDRSWU

'''
Sources used:
https://wiki.archiveteam.org/index.php/YouTube/Technical_details#:~:text=8%20References-,ID%20formats,Za%2Dz0%2D9%2D_%20.

'''

# Variable Creation

def scrape_videos():
    URL_base = "https://www.youtube.com/watch?v="

    reference_ID = [0,0,0,0,0,0,0,0,0,0,0]

    URL_list = ["",
                "",
                "",
                ""]

    average_loop_time = [0,0,0,0,0,0,0,0,0,0]

    data_output_minimal = True

    num_processes = int(input("How many processes would you like to run at once? "))

    # Initializing the URL
    init_from_file = input("Would you like to start the scraper using an URL in a file? ('Y' or 'N') ")
    print("")

    while(not (init_from_file == "Y") and not (init_from_file == "N")):
        print(f"'{init_from_file}' is not a valid input. Please try again.")
        init_from_file = input("Would you like to start the scraper using an URL in a file? ('Y' or 'N') ")

    if(init_from_file == "Y"):
        print("Please put the URL in the first line of 'UnlistedScraperMultiProcessor/LastURL.txt'")
        ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
        print("")

        while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
            print(f"'{ready_to_continue}' is not a valid input. Please try again.")
            init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

        if(ready_to_continue == "STOP"):
            quit()
        else:
            with open("UnlistedScraperMultiProcessor/LastURL.txt","r") as init_file:
                init_URL = init_file.readline().strip("\n")

            while(True):
                if(URL_base in init_URL and len(init_URL) == 43):
                    init_ID = init_URL[32:]

                    valid_ID = func.test_validity(init_ID)

                    if(valid_ID == False): # Invalid input
                        print(f"'{init_URL}' is not a valid input. Please try again.")
                        print("Please put the URL in the first line of 'UnlistedScraperMultiProcessor/LastURL.txt'")
                        ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
                        print("")

                        while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                            print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                            init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                        if(ready_to_continue == "STOP"):
                            quit()
                        else:
                            with open("UnlistedScraperMultiProcessor/LastURL.txt","r") as init_file:
                                init_URL = init_file.readline().strip("\n")
                    else: # Valid input
                        reference_ID = func.initialize_bit_ID(init_ID)
                        break
                else:
                    print(f"'{init_URL}' is not a valid input. Please try again.")
                    print("Please put the URL in the first line of 'UnlistedScraperMultiProcessor/LastURL.txt'")
                    ready_to_continue = input("Is the URL in the file? ('Y' or 'STOP') ")
                    print("")

                    while(ready_to_continue != "Y" and ready_to_continue != "STOP"):
                        print(f"'{ready_to_continue}' is not a valid input. Please try again.")
                        init_from_file = input("Is the URL in the file? ('Y' or 'STOP') ")

                    if(ready_to_continue == "STOP"):
                        quit()
                    else:
                        with open("UnlistedScraperMultiProcessor/LastURL.txt","r") as init_file:
                            init_URL = init_file.readline().strip("\n")
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
                    reference_ID = func.initialize_bit_ID(init_ID)
                    break
            elif(len(init_ID) == 11): # Valid ID input
                # Testing ID for validity
                valid_ID = func.test_validity(init_ID)

                if(valid_ID == False): # Invalid input
                    print(f"'{init_ID}' is not a valid input. Please try again.")
                    init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")
                else: # Valid input
                    reference_ID = func.initialize_bit_ID(init_ID)
                    break
            else: # Invalid input
                print(f"'{init_ID}' is not a valid input. Please try again.")
                init_ID = input("Would you like to start at an initial ID? (input YouTube link, YouTube ID, or 'NONE') ")

    # THIS IS THE CODE FOR MAKING THE URL LIST, OTHER STUFF MAY NOT BE NECESSARY FOR URL
    URL_list, reference_ID = func.make_URL_list(reference_ID, num_processes)

    print("")
    print(f"Current URL: {URL_list[0]}")
    print(f"Current ID: {func.initialize_bit_ID(URL_list[0][32:])}")
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
        if(URL_list[-1][0] == "FINISHED"): # Check for no more IDs
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
            URL_list, reference_ID = func.make_URL_list(reference_ID, num_processes)

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(func.check_for_unlisted_multi, URL_list)
    
        i = 0 
        for URL, is_unlisted in results:
            if(is_unlisted):
                with open("UnlistedScraperMultiProcessor/UnlistedVideos.txt","a") as unlisted_videos:
                    unlisted_videos.write(URL + "\n")

                unlisted_videos_count += 1
                
                print(f"Unlisted Video Found!")
                print(f"Current URL: {URL}")
                print(f"Current ID: {func.initialize_bit_ID(URL[32:])}")

            URLs_tested += 1

        if(data_output_minimal):
            if(URLs_tested % (num_processes * 10) == 0):
                print(f"URLs tested: {URLs_tested}")
                print(f"Average loop time: {func.average_list(average_loop_time):.4f} seconds")
                print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
                print("")
        else:
            print(f"Current URL List: {URL_list}")
            print(f"Current Reference ID: {reference_ID}")
            print(f"Loop Time: {(time.time() - time_start):.4f} seconds")
            print(f"Press 'q' to stop the program. Press 'o' to toggle outputs.")
            print("")

        with open("UnlistedScraperMultiProcessor/LastURL.txt", "w") as file:
            file.write(URL_list[-1])

        del average_loop_time[0]
        average_loop_time.append(time.time() - time_start)

    with open("UnlistedScraperMultiProcessor/TotalURLsTested.txt","r") as total_tested_file:
        total_tested = int(total_tested_file.readline().strip("\n"))
        total_tested += URLs_tested

    with open("UnlistedScraperMultiProcessor/TotalURLsTested.txt","w") as total_tested_file:
        total_tested_file.write(str(total_tested))

    print("")
    print(f"Total Time Elapsed: {(time.time() - loop_start_time):.4f} seconds")
    print(f"Total URLs Tested This Execution: {URLs_tested}")
    print(f"Total URLs Tested: {total_tested}")
    print(f"Total Unlisted Videos Found: {unlisted_videos_count}")
    print(f"Last URL Tested: {URL_list[-1]}")
    print(f"Last ID Tested: {func.initialize_bit_ID(URL_list[-1][32:])}")

if __name__ == "__main__":
    scrape_videos()