def triangle(width):
    if width == 1:
        return 1
    else:
        smaller = triangle(width - 1)
        num = smaller + width
        return num
    
print(triangle(4))