import math
import msvcrt
import func



ID_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
last_ID_chars = "AEIMQUYcgkosw048"

URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]

init_id = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")

while(True):
    if(init_id == "NONE"): # No cur_ID change
        break

    elif(URL_base in init_id and len(init_id) == 33): # Valid YT link input
        init_id = init_id[32:]

        # Testing ID for validity
        valid_chars = True

        i = 0
        for i in range(len(init_id) - 1):
            if(init_id[i] not in ID_chars):
                valid_chars = False

        if(init_id[10] not in ID_chars):
            valid_chars = False

        if(valid_chars == False): # Invalid input
            print(f"{init_id} is not a valid input. Please try again.")
            init_id = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")
        else: # Valid input
            cur_ID = func.initialize_ID(init_id)
            break
    elif(len(init_id) == 11): # Valid ID input
        valid_chars = True

        i = 0
        for i in range(len(init_id) - 1):
            if(init_id[i] not in ID_chars):
                valid_chars = False

        if(init_id[10] not in ID_chars):
            valid_chars = False

        if(valid_chars == False): # Invalid input
            print(f"{init_id} is not a valid input. Please try again.")
            init_id = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")
        else: # Valid input
            cur_ID = func.initialize_ID(init_id)
            break
    else: # Invalid input

        print(f"{init_id} is not a valid input. Please try again.")
        init_id = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")

