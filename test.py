with open('file.txt' , 'r' ) as file_1:
    for line in file_1:
        print(line)
    lines = file_1.readlines()
    print(lines)