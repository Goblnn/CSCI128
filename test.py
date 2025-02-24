def func(x,y):
    print(x+y)
    return (x-y) ** 2

values = [1,5,9,7,2,4]

for i in range(len(values)):
    a = values[i-1]
    b = func(a,i)
    print("")
    print(i)
    print(a)
    print(b)
    print("")