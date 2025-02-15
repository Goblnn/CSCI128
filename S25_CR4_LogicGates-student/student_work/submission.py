# Assesment 4 Code Review

gate_to_test = input("Enter gate: ")
first_input = input("Enter first input: ")
second_input = input("Enter second input: ")

# Define valid gates and inputs
valid_gates = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
valid_inputs = ["0", "1"]

# Check if the gate and inputs are valid
if gate_to_test not in valid_gates:
    print(f'OUTPUT Invalid Gate {gate_to_test}')
elif first_input not in valid_inputs:
    print(f'OUTPUT Invalid Input {first_input}')
elif second_input not in valid_inputs:
    print(f'OUTPUT Invalid Input {second_input}')
else:
    a = int(first_input)
    b = int(second_input)
    
    if gate_to_test == "AND":
        if a == True and b == True:
            result = True
        else:
            result = False
    elif gate_to_test == "OR":
        if (a == True and b == True) or (a == True and b == False) or (a == False and b == True):
            result = True
        else:
            result = False
    elif gate_to_test == "NAND":
        if not (a == True and b == True):
            result = True
        else:
            result = False
    elif gate_to_test == "NOR":
        if not (a == True or b == True):
            result = True
        else:
            result = False
    elif gate_to_test == "XOR":
        if (a == True and b == False) or (a == False and b == True):
            result = True
        else:
            result = False
    elif gate_to_test == "XNOR":
        if (a == True and b == True) or (a == False and b == False):
            result = True
        else:
            result = False

    # Output the result
    if result:
        print('OUTPUT True')
    else:
        print('OUTPUT False')