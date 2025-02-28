import math
import msvcrt
import func
import time
from urllib.request import urlopen

# public link: https://www.youtube.com/watch?v=Ipw0NZThxKo
# unlisted link: https://www.youtube.com/watch?v=RFWk_NDRSWU

'''
Sources used:
https://wiki.archiveteam.org/index.php/YouTube/Technical_details#:~:text=8%20References-,ID%20formats,Za%2Dz0%2D9%2D_%20.

'''

URL_base = "https://www.youtube.com/watch?v="

unlisted_badge = '<p class="style-scope ytd-badge-supported-renderer">Unlisted</p>'

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
time_start = time.time()
page = urlopen(cur_URL)
html_bytes = page.read()

html_string = html_bytes.decode("utf-8")


f = open("vidhtml.txt","w")
f.write(html_string)
# print(html_string)

if(unlisted_badge in html_string):
    print("LOCKED IN")
else:
    print("LOCKED OUT")
print(time.time() - time_start)