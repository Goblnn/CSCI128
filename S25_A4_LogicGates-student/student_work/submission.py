# Isaac Lane
# CSCI 128 - Section K
# Assessment 4
# References: no one
# Time: 

gate = input("GATE> ")
input1 = int(input("INP1> "))
input2 = int(input("INP2> "))

valid_gates = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]

if(gate not in valid_gates):
    print(f"OUTPUT Invalid Gate {gate}")
elif(input1 != 1 and input1 != 0):
    print(f"OUTPUT Invalid Input {input1}")
elif(input2 != 1 and input2 != 0):
    print(f"OUTPUT Invalid Input {input2}")
else:
    if(input1 == 1):
        x = True
    else:
        x = False

    if(input2 == 1):
        y = True
    else:
        y = False

    if(gate == "AND"):
        print(f"OUTPUT {x and y}")
    elif(gate == "OR"):
        print(f"OUTPUT {x or y}")
    elif(gate == "NAND"):
        print(f"OUTPUT {not (x and y)}")
    elif(gate == "NOR"):
        print(f"OUTPUT {not (x or y)}")
    elif(gate == "XOR"):
        print(f"OUTPUT {x != y}")
    elif(gate == "XNOR"):
        print(f"OUTPUT {x == y}")