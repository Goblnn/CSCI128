# Isaac Lane
# CSCI 128 - Section K
# Assessment 5
# References: no one
# Time: 1 hour

import math

bat = int(input("BATTERY> "))
temp = int(input("HEAT> "))

x_coord = 0
y_coord = 0

num_moves = 0

while(bat > 10 and temp < 125):
    inp = input("COORD> ")

    if(inp == "DONE"):
        break

    inp = inp.split()

    x = float(inp[0])
    y = float(inp[1])

    distance_moved = math.sqrt((x - x_coord)**2 + (y - y_coord)**2)
    bat_change = int(abs(distance_moved // 2))
    temp_change = bat_change * 5
    
    bat -= bat_change
    temp += temp_change

    x_coord = x
    y_coord = y

    print(f"OUTPUT Distance: {distance_moved:.2f} Battery: {bat}")
    num_moves += 1

print(f"OUTPUT {num_moves}")
print(f"OUTPUT {x_coord:.2f} {y_coord:.2f}")
print(f"OUTPUT {int(temp)}")
print(f"OUTPUT {int(bat)}")