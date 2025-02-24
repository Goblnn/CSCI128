l = [1, 2, 3]
i = 999

def change(l, i):
    l[0] = "changed"
    i = 0

print(f"l: { l} , i: { i} ")
change(l, i)
print(f"l: { l} , i: { i} ")