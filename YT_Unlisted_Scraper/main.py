import math
import msvcrt
import func

URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]
cur_URL = ""

init_ID = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")

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

print("Scraping is starting")
print("")

