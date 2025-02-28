import math
import msvcrt
import func

ID_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
last_ID_chars = "AEIMQUYcgkosw048"

URL_base = "https://www.youtube.com/watch?v="

cur_ID = [0,0,0,0,0,0,0,0,0,0,0]

init_id = input("Start at initial ID? (input YT link, id, or 'NONE')")

while(True):
    if(init_id == "NONE"):
        break

    elif(URL_base in init_id and len(init_id) == 33):
        init_id = init_id[32:]
        break

    elif(len(init_id) == 11):
        valid_chars = True


        for i in range(len(cur_ID) - 1):
            cur_ID[i] = ID_chars.index(init_id[i])
        
        cur_ID[10] = last_ID_chars.index(init_id[10])
        break

    else:
        # Invalid inputs

        print(f"{init_id} is not a valid input. Please try again.")
        init_id = input("Start at initial ID? (input YouTube link, YouTube ID, or 'NONE')")