# Isaac Lane
# CSCI 128 - Section K
# Assessment 4
# References: no one
# Time: 

gate = input()
input1 = int(input())
input2 = int(input())

valid_gates = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]

if(gate not in valid_gates):
    print(f"OUTPUT Invalid Gate {gate}")
elif(input1 != 1 and input1 != 0):
    print(f"OUTPUT Invalid Input {input1}")
elif(input2 != 1 and input2 != 0):
    print(f"OUTPUT Invalid Input {input2}")