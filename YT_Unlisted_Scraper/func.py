ID_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
last_ID_chars = "AEIMQUYcgkosw048"

def initialize_ID(ID):
    new_ID = [0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    for i in range(len(ID) - 1):
        new_ID[i] = ID_chars.index(ID[i])
    
    new_ID[10] = last_ID_chars.index(ID[10])
    
    return ID