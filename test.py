output = ""
my_list = [1, 3, 0]
for num in my_list:
    for i in range(0, num):
        output += f"{i} "
print(output)