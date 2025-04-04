# Isaac Lane
# CSCI128 - Section K
# Python-DieRolls

import matplotlib.pyplot as plt

inp = input()
lst = []
while inp != "DONE":
    lst.append(int(inp)
    inp = input()
    
    
numbers = []
times = []
for num in lst:
    if num not in numbers:
        numbers.append(num)
        times.append(1)
    else:
        index = numbers.index(num)
        times[index] +=1
        
plt.bar(numbers, times)

plt.savefig("rolls_bar_chart.png")